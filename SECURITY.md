# Security: PAT for CI push fallback

This repository uses GitHub Actions workflows that may need to push generated files back to branches when run in CI (for example, regenerated `*.freezed.dart` files from Flutter `freezed` codegen).

When possible we prefer the built-in `GITHUB_TOKEN` (ephemeral, scoped to the workflow) to perform pushes. However, some repositories use branch protection rules that prevent `GITHUB_TOKEN` from pushing. In those cases, we support a fallback that uses a Personal Access Token (PAT) stored as a repository secret named `ACTIONS_PAT`.

How to create a Personal Access Token (PAT)

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** (classic) or **Generate new token (classic)** depending on your account UI.
3. Give the token a descriptive name, e.g. `actions-codegen-bot-2025-11`.
4. Select the following scopes (minimum recommended):
   - `repo` (Full control of private repositories) — required for pushing to repository.
   - `workflow` (Update GitHub Action workflow runs) — optional, only if your workflows need to manage workflows.

   Note: If you want to limit the token further, create a dedicated machine user with access only to the repositories required and grant `repo` scope for those repositories.

5. Generate the token and copy it. Treat it like a secret — do not paste it in chat or code.

Add PAT as repository secret

1. In the repository, go to **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Use the following values:
   - **Name**: `ACTIONS_PAT`
   - **Value**: the PAT you generated
4. Click **Add secret**.

Workflow behavior and security notes

- The `freezed` codegen workflow will attempt to push generated files using `GITHUB_TOKEN` first. If that push fails due to branch protections, it will retry using the `ACTIONS_PAT` secret.
- The PAT is long-lived; rotate it periodically and scope it narrowly. Prefer using a machine account rather than a personal account where possible.
- Only add `ACTIONS_PAT` to repositories where you accept the security tradeoff; document ownership and rotation schedule for the PAT in your team's vault or secrets manager.

If you need help creating a machine user or setting up an automated rotation policy, ask the security/infra team for recommended best practices in your organization.
