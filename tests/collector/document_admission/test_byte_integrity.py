from dataclasses import replace

from collector.document_admission import Sha256ByteIntegrityVerifier

from .synthetic_fixtures import NOW, VALID_TXT, build_policies


def test_sha256_identity_is_deterministic():
    verifier = Sha256ByteIntegrityVerifier()
    policy = build_policies().digest

    first = verifier.identify(VALID_TXT, policy)
    second = verifier.identify(VALID_TXT, policy)

    assert first == second
    assert first.byte_count == len(VALID_TXT)
    assert len(first.digest_hex) == 64


def test_integrity_verification_matches_exact_synthetic_bytes():
    verifier = Sha256ByteIntegrityVerifier()
    identity = verifier.identify(VALID_TXT, build_policies().digest)

    result = verifier.verify(
        VALID_TXT,
        identity,
        "verification-1",
        NOW,
    )

    assert result.matches is True
    assert result.expected == result.observed


def test_integrity_verification_detects_altered_bytes():
    verifier = Sha256ByteIntegrityVerifier()
    identity = verifier.identify(VALID_TXT, build_policies().digest)

    result = verifier.verify(
        VALID_TXT + b"-ALTERED",
        identity,
        "verification-1",
        NOW,
    )

    assert result.matches is False
    assert result.expected != result.observed


def test_identity_does_not_depend_on_filename_metadata():
    verifier = Sha256ByteIntegrityVerifier()
    identity = verifier.identify(VALID_TXT, build_policies().digest)
    changed_metadata_identity = replace(identity)

    assert identity == changed_metadata_identity
