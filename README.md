# Tiraz (طِرَاز) - AI Tailoring App (FastAPI + Flutter)

This is the official repository for the **"Tiraz"** application, an MVP (Minimum Viable Product) aiming to revolutionize custom tailoring by using AI for body measurements.

**Current Status**: Sprint 0 (Boilerplate Setup) is **COMPLETE**.  
The **main** branch is 100% clean, healthy, and ready for Sprint 1 development to begin.

---

## 🏗️ Tech Stack (The Official Stack)

The one and only approved tech stack for this project is:

- **Backend**: FastAPI (Python)
- **Mobile App**: Flutter (Dart)
- **Database**: PostgreSQL
- **Infrastructure**: Docker (via docker-compose)
- **CI/Quality**: GitHub Actions (using ruff & black)

*(Note: All legacy use of Node.js, Express, React Native, Flask, or MongoDB has been permanently removed from this project.)*

---

## 🚀 Quick Start (via Docker)

This project is fully containerized with Docker Compose.

### Prerequisites
- Docker
- Docker Compose

### Running (for Local Development)

```bash
# 1. Get the latest code from main
git checkout main
git pull origin main

# 2. Build and run all services (backend + database)
# This will also build the Flutter app container if defined
docker-compose up --build -d

# 3. (Optional) Check that services are running
docker-compose ps
```

### Accessing Services
- **Backend (FastAPI)**: http://localhost:8000
- **Health Check Endpoint**: http://localhost:8000/health
- **Database (PostgreSQL)**: Accessible on port 5432 (for tools like DBeaver)

### Stopping Services

```bash
# Stop all services
docker-compose down
```

---

## 📁 Project Structure

```
Tiraz/
├── .github/
│   └── workflows/
│       └── ci.yml          # (FastAPI CI Quality Check)
├── backend/                # (FastAPI - Python Project)
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── mobile-app/             # (Flutter - Dart Project)
│   ├── lib/
│   │   └── main.dart
│   ├── Dockerfile
│   └── pubspec.yaml
├── docker-compose.yml      # (Main project orchestrator)
├── BOILERPLATE_SETUP_COMPLETE.md # (Sprint 0 Completion Doc)
└── README.md               # (This file)
```

---

## 🧪 Testing & Quality (CI)

We use **GitHub Actions** to run automated CI checks on every PR targeting main:

- **ruff**: For Python code error linting.
- **black**: To ensure consistent code formatting.

---

## 🤝 Contributing

1. Create a new feature branch (`git checkout -b feat/my-new-feature`)
2. Make your changes.
3. Push your changes (`git push ...`)
4. Open a Pull Request for review.

---

## 📄 License

This project is licensed under the MIT License.
