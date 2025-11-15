# Flutter Freezed Codegen Instructions

This file documents how to run Flutter codegen locally (for `freezed` + `build_runner`) and how to commit generated files so PR #71 can be verified.

Prerequisites
- Have Flutter SDK installed and on your PATH. Tested with Flutter >= 3.0.
- Have `dart` and `flutter` commands available.
- Run from repo root. You may want to use the same Flutter channel/version used by CI; check `.github/workflows` if needed.

Quick steps (local)

1. Open a shell and change to the mobile app directory:

```bash
cd mobile-app
```

2. Ensure Flutter is available and on the expected channel:

```bash
flutter --version
# Optional: switch channel if CI uses stable
flutter channel stable
flutter upgrade
```

3. Get packages:

```bash
flutter pub get
```

4. Run build_runner to generate freezed files:

```bash
# Clean previous generated artifacts first (optional but recommended)
flutter pub run build_runner clean

# Generate files (non-watch mode)
flutter pub run build_runner build --delete-conflicting-outputs
```

Notes on flags:
- `--delete-conflicting-outputs` is recommended when upgrading `freezed` to avoid conflicts.
- Use `watch` during development for incremental generation:
  `flutter pub run build_runner watch --delete-conflicting-outputs`

What to commit
- Generated files are typically named `*.freezed.dart` and `*.g.dart`.
- We removed the temporary analyzer exclusion, so generated files should be committed to the branch.
- Commit only generated files that are tracked by Git (do not commit build or .dart_tool caches).

Commit example:

```bash
# From repo root
git checkout feature/sprint4-freezed-upgrade
cd mobile-app
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
# Add generated files
git add lib/**/*.freezed.dart lib/**/*.g.dart
git commit -m "chore(mobile): generated freezed files after upgrade"
git push origin feature/sprint4-freezed-upgrade
```

CI considerations
- If CI runs `flutter pub get` and `build_runner` in a workflow, ensure the workflow has sufficient SDK and disk space.
- If generation fails on CI, try running the same commands locally with the same Flutter version and compare errors.

If you want, I can add a small GitHub Actions job snippet to run generation in CI and push the generated files back to the branch automatically (requires a PAT with repo write access). Let me know if you'd like that.
