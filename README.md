# Tiraz — FastAPI + Flutter Boilerplate

This repository replaces the previous contents with a complete boilerplate:

- Backend: FastAPI (async, OpenAPI docs, JWT-ready)
- Mobile: Flutter (skeleton & README)
- Dev infra: Dockerfile(s) + docker-compose, CI skeleton
- AI service: placeholder service to host Python AI models (can be the existing ai-models code)

Branch: `copilot/fastapi-flutter-boilerplate`

High level structure:
- backend/
  - app/
    - main.py
    - routes/
      - measurement.py
  - requirements.txt
  - Dockerfile
- mobile/
  - flutter_app/ (Flutter project skeleton placeholder)
  - README.md
- docker-compose.yml
- .gitignore

Next step (after you confirm): I will push these files to the branch `copilot/fastapi-flutter-boilerplate` and open a PR if you want. After pushing I will:
- Create issues for remaining migration work (auth, models, DB migrations, AI integration).
- Run a quick CI build to verify the Docker image builds.
