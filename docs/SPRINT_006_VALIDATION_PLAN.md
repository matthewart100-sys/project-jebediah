SPRINT 006 — Validation Plan

Purpose
-------
This validation plan documents the concrete checks, acceptance criteria, and test artifacts required to prepare the feature/interaction-gateway branch for the VBA executive demonstration.

Scope
-----
Covers Interaction Gateway changes made on branch feature/interaction-gateway and their integration with:
- Jebediah Memory Service
- Ollama embedding provider and local model runtime
- Qdrant vector store

Non-goals
---------
- Changing Sprint 005 memory architecture
- Modifying Qdrant or embedding identity contracts
- Merging ADRs (they remain Proposed)

Acceptance criteria
-------------------
1. Interaction Gateway provides deterministic context assembly and consumes memory responses structurally.
2. Interaction Gateway API (/chat) tests exist and pass for:
   - Success path
   - Memory service unavailable (503)
   - Ollama / embedding provider unavailable (503)
   - Structured context handling (deterministic ordering)
3. Demo control scripts exist: scripts/demo_start.sh, scripts/demo_stop.sh
4. Demo readiness documentation updated and references demo_start/demo_stop and deterministic context behavior.
5. Automated validation steps complete locally on the demo VM:
   - pytest (interaction tests)
   - docker build for the interaction service
   - scripts/demo_check.sh returns success or clear actionable failures

Test plan
---------
- Unit / integration tests (pytest): tests/services/test_interaction_chat.py
  - Use FastAPI TestClient to exercise /chat endpoint with monkeypatching to simulate memory and generation providers.
- Manual / integration checks:
  - docker compose build of services/jebediah-interaction
  - scripts/demo_check.sh when containers are running

Execution checklist
-------------------
1. Code changes merged on feature/interaction-gateway branch.
2. Run pytest locally: pytest -q tests/services/test_interaction_chat.py
3. Build interaction image: docker build -f services/jebediah-interaction/Dockerfile -t jebediah-interaction:local .
4. Start required containers and run scripts/demo_check.sh. Follow remediation guidance in docs/DEMO_READINESS.md if failures occur.

Artifacts to collect
--------------------
- pytest results and output
- docker build output (interaction image)
- scripts/demo_check.sh output (network and service reachability)
- A copy of the end-to-end /chat request and response demonstrating context and evidence attachment

Risks and mitigations
---------------------
- Ollama container unreachable from docker network: provide step-by-step instructions in docs/DEMO_READINESS.md and demo_start script to attach Ollama to the network or guide host binding.
- Non-deterministic context assembly: enforce sorting and stable rendering in context_builder (done in this sprint).

Owner
-----
Pilot Stabilization Engineer (implementation) — prepares artifacts and verifies checks.
Architecture review remains required for ADR acceptance; do not auto-merge ADRs.

Document version: 1.0
