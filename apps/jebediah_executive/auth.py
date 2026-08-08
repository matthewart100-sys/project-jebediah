"""Authentication and session runtime for the Executive Shell.

This module provides bounded local authentication, role/organization/workspace
authorization, secure session management, account lockout, and password reset
token architecture without introducing external service dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value > 0 else default


@dataclass(frozen=True)
class PlatformUser:
    user_id: str
    display_name: str
    email: str
    password_hash: str
    organization_memberships: tuple[str, ...]
    workspace_permissions: tuple[str, ...]
    role: str
    status: str
    created_at: datetime
    last_login_at: datetime | None
    failed_login_attempts: int
    lockout_until: datetime | None
    audit_metadata: tuple[str, ...]


@dataclass(frozen=True)
class AuthSession:
    session_id: str
    user_id: str
    issued_at: datetime
    expires_at: datetime
    remember_device: bool
    csrf_token: str
    selected_workspace_mode: str
    selected_organization_id: str


@dataclass(frozen=True)
class LoginResult:
    session: AuthSession | None
    error: str | None


@dataclass(frozen=True)
class SessionResolution:
    session: AuthSession | None
    user: PlatformUser | None
    expired: bool


_ALL_WORKSPACE_MODES = ("demonstration", "development", "production")
_ALL_ROLES = (
    "platform_administrator",
    "organization_administrator",
    "executive",
    "reviewer",
    "operator",
    "viewer",
)
_ACTIVE_STATUS = "active"
_LOCKED_STATUS = "locked"
_DISABLED_STATUS = "disabled"


def _hash_password(password: str, *, salt_hex: str | None = None) -> str:
    if not password:
        raise ValueError("password cannot be empty")
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return f"pbkdf2_sha256$200000${salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, rounds_raw, salt_hex, digest_hex = stored_hash.split("$", 3)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    try:
        rounds = int(rounds_raw)
    except ValueError:
        return False
    computed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        rounds,
    ).hex()
    return hmac.compare_digest(computed, digest_hex)


class AuthRuntime:
    """Local authentication runtime with persisted user model."""

    def __init__(self, runtime_root: Path) -> None:
        self._runtime_root = runtime_root
        self._auth_dir = runtime_root / "auth"
        self._auth_dir.mkdir(parents=True, exist_ok=True)
        self._users_path = self._auth_dir / "users.json"
        self._sessions: dict[str, AuthSession] = {}
        self._reset_tokens: dict[str, tuple[str, datetime]] = {}
        self._audit_events: list[tuple[datetime, str, str, str]] = []
        self._session_timeout_minutes = _env_int("BONSAAI_SESSION_TIMEOUT_MINUTES", 30)
        self._remember_days = _env_int("BONSAAI_REMEMBER_DEVICE_DAYS", 30)
        self._lockout_threshold = _env_int("BONSAAI_LOCKOUT_ATTEMPTS", 5)
        self._lockout_minutes = _env_int("BONSAAI_LOCKOUT_MINUTES", 15)
        self._users = self._load_or_bootstrap_users()

    @property
    def users(self) -> tuple[PlatformUser, ...]:
        return tuple(self._users.values())

    @property
    def active_session_count(self) -> int:
        self._prune_sessions()
        return len(self._sessions)

    @property
    def locked_account_count(self) -> int:
        now = _now()
        return sum(
            1
            for user in self._users.values()
            if user.status == _LOCKED_STATUS
            and user.lockout_until is not None
            and user.lockout_until > now
        )

    @property
    def audit_events(self) -> tuple[tuple[datetime, str, str, str], ...]:
        return tuple(self._audit_events)

    def _record_audit(self, event: str, user_id: str, detail: str) -> None:
        self._audit_events.append((_now(), event, user_id, detail))

    def _load_or_bootstrap_users(self) -> dict[str, PlatformUser]:
        if self._users_path.exists():
            raw = self._read_user_store()
            users = self._load_users(raw)
            if users or not self._has_valid_empty_user_store(raw):
                return users
        users = self._bootstrap_users_from_env()
        self._save_users(users)
        return users

    def _read_user_store(self) -> object | None:
        try:
            return json.loads(self._users_path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return None

    @staticmethod
    def _has_valid_empty_user_store(raw: object) -> bool:
        """Return whether the persisted store is valid and explicitly empty."""
        return isinstance(raw, dict) and raw.get("users") == []

    def _bootstrap_users_from_env(self) -> dict[str, PlatformUser]:
        email = os.getenv("BONSAAI_BOOTSTRAP_ADMIN_EMAIL", "").strip().lower()
        password = os.getenv("BONSAAI_BOOTSTRAP_ADMIN_PASSWORD", "").strip()
        display_name = (
            os.getenv("BONSAAI_BOOTSTRAP_ADMIN_DISPLAY_NAME", "").strip()
            or "Platform Administrator"
        )
        organization_id = (
            os.getenv("BONSAAI_BOOTSTRAP_ADMIN_ORGANIZATION", "").strip().lower()
            or "virginia-b-andes"
        )
        if not email or not password:
            return {}
        user = PlatformUser(
            user_id="user-platform-admin",
            display_name=display_name,
            email=email,
            password_hash=_hash_password(password),
            organization_memberships=(organization_id,),
            workspace_permissions=("development", "production"),
            role="platform_administrator",
            status=_ACTIVE_STATUS,
            created_at=_now(),
            last_login_at=None,
            failed_login_attempts=0,
            lockout_until=None,
            audit_metadata=("bootstrap_admin",),
        )
        return {user.user_id: user}

    def _load_users(self, raw: object) -> dict[str, PlatformUser]:
        if not isinstance(raw, dict):
            return {}
        users: dict[str, PlatformUser] = {}
        for payload in raw.get("users", []):
            user = PlatformUser(
                user_id=str(payload.get("user_id", "")).strip(),
                display_name=str(payload.get("display_name", "")).strip(),
                email=str(payload.get("email", "")).strip().lower(),
                password_hash=str(payload.get("password_hash", "")).strip(),
                organization_memberships=tuple(payload.get("organization_memberships", ())),
                workspace_permissions=tuple(payload.get("workspace_permissions", ())),
                role=str(payload.get("role", "")).strip(),
                status=str(payload.get("status", _DISABLED_STATUS)).strip(),
                created_at=datetime.fromisoformat(payload.get("created_at")),
                last_login_at=(
                    datetime.fromisoformat(payload.get("last_login_at"))
                    if payload.get("last_login_at")
                    else None
                ),
                failed_login_attempts=int(payload.get("failed_login_attempts", 0)),
                lockout_until=(
                    datetime.fromisoformat(payload.get("lockout_until"))
                    if payload.get("lockout_until")
                    else None
                ),
                audit_metadata=tuple(payload.get("audit_metadata", ())),
            )
            if user.user_id and user.role in _ALL_ROLES:
                users[user.user_id] = user
        return users

    def _save_users(self, users: dict[str, PlatformUser]) -> None:
        payload = {
            "users": [
                {
                    "user_id": user.user_id,
                    "display_name": user.display_name,
                    "email": user.email,
                    "password_hash": user.password_hash,
                    "organization_memberships": list(user.organization_memberships),
                    "workspace_permissions": list(user.workspace_permissions),
                    "role": user.role,
                    "status": user.status,
                    "created_at": user.created_at.isoformat(),
                    "last_login_at": user.last_login_at.isoformat()
                    if user.last_login_at
                    else None,
                    "failed_login_attempts": user.failed_login_attempts,
                    "lockout_until": user.lockout_until.isoformat()
                    if user.lockout_until
                    else None,
                    "audit_metadata": list(user.audit_metadata),
                }
                for user in users.values()
            ]
        }
        self._users_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        os.chmod(self._users_path, 0o600)

    def _prune_sessions(self) -> None:
        now = _now()
        stale = [session_id for session_id, session in self._sessions.items() if session.expires_at <= now]
        for session_id in stale:
            self._sessions.pop(session_id, None)

    def _find_user_by_email(self, email: str) -> PlatformUser | None:
        lowered = email.strip().lower()
        for user in self._users.values():
            if user.email == lowered:
                return user
        return None

    def login(
        self,
        *,
        email: str,
        password: str,
        remember_device: bool,
    ) -> LoginResult:
        user = self._find_user_by_email(email)
        if user is None:
            return LoginResult(session=None, error="invalid_credentials")
        now = _now()
        if (
            user.status == _LOCKED_STATUS
            and user.lockout_until is not None
            and user.lockout_until > now
        ):
            self._record_audit("auth.login_locked", user.user_id, "account_locked")
            return LoginResult(session=None, error="account_locked")
        if user.status == _DISABLED_STATUS:
            return LoginResult(session=None, error="account_disabled")
        if not _verify_password(password, user.password_hash):
            failed_attempts = user.failed_login_attempts + 1
            lockout_until = None
            status = user.status
            if failed_attempts >= self._lockout_threshold:
                status = _LOCKED_STATUS
                lockout_until = now + timedelta(minutes=self._lockout_minutes)
            updated = PlatformUser(
                user_id=user.user_id,
                display_name=user.display_name,
                email=user.email,
                password_hash=user.password_hash,
                organization_memberships=user.organization_memberships,
                workspace_permissions=user.workspace_permissions,
                role=user.role,
                status=status,
                created_at=user.created_at,
                last_login_at=user.last_login_at,
                failed_login_attempts=failed_attempts,
                lockout_until=lockout_until,
                audit_metadata=user.audit_metadata,
            )
            self._users[user.user_id] = updated
            self._save_users(self._users)
            self._record_audit("auth.login_failed", user.user_id, "invalid_password")
            return LoginResult(session=None, error="invalid_credentials")

        ttl = (
            timedelta(days=self._remember_days)
            if remember_device
            else timedelta(minutes=self._session_timeout_minutes)
        )
        session = AuthSession(
            session_id=secrets.token_urlsafe(32),
            user_id=user.user_id,
            issued_at=now,
            expires_at=now + ttl,
            remember_device=remember_device,
            csrf_token=secrets.token_urlsafe(24),
            selected_workspace_mode="demonstration",
            selected_organization_id=(
                user.organization_memberships[0]
                if user.organization_memberships
                else "demo-organization"
            ),
        )
        self._sessions[session.session_id] = session
        refreshed = PlatformUser(
            user_id=user.user_id,
            display_name=user.display_name,
            email=user.email,
            password_hash=user.password_hash,
            organization_memberships=user.organization_memberships,
            workspace_permissions=user.workspace_permissions,
            role=user.role,
            status=_ACTIVE_STATUS,
            created_at=user.created_at,
            last_login_at=now,
            failed_login_attempts=0,
            lockout_until=None,
            audit_metadata=user.audit_metadata,
        )
        self._users[user.user_id] = refreshed
        self._save_users(self._users)
        self._record_audit("auth.login_success", user.user_id, "session_created")
        return LoginResult(session=session, error=None)

    def resolve_session(self, session_id: str | None) -> SessionResolution:
        if not session_id:
            return SessionResolution(session=None, user=None, expired=False)
        self._prune_sessions()
        session = self._sessions.get(session_id)
        if session is None:
            return SessionResolution(session=None, user=None, expired=True)
        user = self._users.get(session.user_id)
        if user is None or user.status == _DISABLED_STATUS:
            self._sessions.pop(session_id, None)
            return SessionResolution(session=None, user=None, expired=True)
        return SessionResolution(session=session, user=user, expired=False)

    def renew_session(self, session: AuthSession) -> AuthSession:
        ttl = (
            timedelta(days=self._remember_days)
            if session.remember_device
            else timedelta(minutes=self._session_timeout_minutes)
        )
        renewed = AuthSession(
            session_id=session.session_id,
            user_id=session.user_id,
            issued_at=session.issued_at,
            expires_at=_now() + ttl,
            remember_device=session.remember_device,
            csrf_token=session.csrf_token,
            selected_workspace_mode=session.selected_workspace_mode,
            selected_organization_id=session.selected_organization_id,
        )
        self._sessions[renewed.session_id] = renewed
        return renewed

    def logout(self, session_id: str | None) -> None:
        if not session_id:
            return
        session = self._sessions.pop(session_id, None)
        if session is not None:
            self._record_audit("auth.logout", session.user_id, "session_invalidated")

    def update_workspace_selection(
        self,
        *,
        session: AuthSession,
        workspace_mode: str,
        organization_id: str,
    ) -> AuthSession:
        normalized_mode = workspace_mode.strip().lower()
        if normalized_mode not in _ALL_WORKSPACE_MODES:
            raise ValueError("unsupported_workspace_mode")
        user = self._users.get(session.user_id)
        if user is None:
            raise RuntimeError("unknown_user")
        if organization_id not in user.organization_memberships and normalized_mode != "demonstration":
            raise ValueError("organization_access_denied")
        if normalized_mode == "development" and "development" not in user.workspace_permissions:
            raise ValueError("workspace_access_denied")
        if normalized_mode == "production" and "production" not in user.workspace_permissions:
            raise ValueError("workspace_access_denied")
        updated = AuthSession(
            session_id=session.session_id,
            user_id=session.user_id,
            issued_at=session.issued_at,
            expires_at=session.expires_at,
            remember_device=session.remember_device,
            csrf_token=session.csrf_token,
            selected_workspace_mode=normalized_mode,
            selected_organization_id=organization_id,
        )
        self._sessions[updated.session_id] = updated
        return updated

    def request_password_reset(self, email: str) -> str | None:
        user = self._find_user_by_email(email)
        if user is None:
            return None
        token = secrets.token_urlsafe(32)
        self._reset_tokens[token] = (user.user_id, _now() + timedelta(hours=1))
        self._record_audit("auth.password_reset_requested", user.user_id, "token_issued")
        return token

    def reset_password(self, *, token: str, new_password: str) -> bool:
        payload = self._reset_tokens.get(token)
        if payload is None:
            return False
        user_id, expires_at = payload
        if expires_at <= _now():
            self._reset_tokens.pop(token, None)
            return False
        user = self._users.get(user_id)
        if user is None:
            return False
        updated = PlatformUser(
            user_id=user.user_id,
            display_name=user.display_name,
            email=user.email,
            password_hash=_hash_password(new_password),
            organization_memberships=user.organization_memberships,
            workspace_permissions=user.workspace_permissions,
            role=user.role,
            status=_ACTIVE_STATUS,
            created_at=user.created_at,
            last_login_at=user.last_login_at,
            failed_login_attempts=0,
            lockout_until=None,
            audit_metadata=user.audit_metadata,
        )
        self._users[user.user_id] = updated
        self._save_users(self._users)
        self._reset_tokens.pop(token, None)
        self._record_audit("auth.password_reset_completed", user.user_id, "password_changed")
        return True
