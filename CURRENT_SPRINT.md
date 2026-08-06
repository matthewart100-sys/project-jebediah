# Current Sprint

## Active sprint

**Name:** Operational Workspace Implementation Sprint

**Status:** Active under Chief Architect directive to complete multi-workspace
operations within the existing Executive Shell, with no architecture redesign,
governance changes, or duplicate runtime implementations.

**Deployment status:** Authorized (operational workspace integration)

**Information-use status:** Workspace controls must preserve governed
information boundaries and prevent cross-workspace data leakage.

## Active milestone question

Can Bonsaai run demonstration, development, and production workspaces from one
Executive Shell with persistent selection, strict runtime separation, and no
application redeploy?

## Authorized milestone boundary

This sprint authorizes:

- workspace mode selection (demo/development/production);
- organization configuration selection at startup/landing;
- persistent workspace state;
- workspace banner and safeguards;
- demonstration reset behavior;
- deployment/runtime configuration updates for workspace defaults;
- documentation and validation updates required by this work.

This sprint does **not** authorize:

- new business capabilities;
- architecture or governance redesign;
- replacement or duplication of existing runtime pipelines.

## Success criteria

1. Workspace and organization selection are integrated into the existing shell.
2. Demonstration reset is available and restores synthetic baseline behavior.
3. Development and production runtime state are isolated.
4. Deployment package supports workspace startup configuration.
5. Validation passes for tests, docs, and repository checks.
