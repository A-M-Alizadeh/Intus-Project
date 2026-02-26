---
title: Intus Project
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Intus – MedTech Mini Web-App

This repository contains:

- `backend/`: Django API for medical-image phase simulation.
- `frontend/`: Vue + Vite UI for upload, phase selection, and side-by-side display.

## How the app works (simple)

1. Open the frontend page.
2. Upload a medical image (`.png`, `.jpg`, or `.jpeg`).
3. Select one phase:
   - **Arterial**: increases image contrast.
   - **Venous**: applies gaussian smoothing (soft blur).
4. Click process.
5. The frontend sends your image + selected phase to the backend API (`/api/imaging/process/`).
6. The backend processes the image and returns the result.
7. The frontend shows original and processed images side by side.

## Local run (without Docker)

### 1) Backend (Django)

```bash
cd /Users/graybook/Documents/Projects/Interview/Intus
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements/base.txt
cp .env.example .env
python backend/manage.py migrate
python backend/manage.py runserver 0.0.0.0:8000
```

### 2) Frontend (Vue)

In another terminal:

```bash
cd /Users/graybook/Documents/Projects/Interview/Intus/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Open:

- Frontend: `http://127.0.0.1:5173`
- Backend API: `http://127.0.0.1:8000/api/imaging/process/`

The frontend reads `VITE_API_BASE_URL`; if unset, it falls back to `http://127.0.0.1:8000`.

## Docker Compose (backend + frontend)

From repo root:

```bash
docker compose up --build
```

Open:

- Frontend: `http://127.0.0.1:5173`
- Backend: `http://127.0.0.1:8000`

Stop:

```bash
docker compose down
```

## Deploy backend to Hugging Face Spaces (Docker)

1. Create a new **Space** on Hugging Face:
   - SDK: **Docker**
   - Visibility: your choice
2. In the Space repo, use `backend/Dockerfile.hf` as the Dockerfile content (or copy it to `Dockerfile` in the Space root).
3. In Space **Settings → Variables and secrets**, set:
   - `DJANGO_SETTINGS_MODULE=config.settings.docker`
   - `SECRET_KEY=<strong-random-secret>`
   - `ALLOWED_HOSTS=*` (or your HF domain)
4. After build is green, copy your Space URL, e.g. `https://<space-name>.hf.space`.

## Deploy frontend to GitHub Pages (Vue + Vite)

1. In `frontend/vite.config.js`, set the correct base path:
   - For repo pages: `base: '/<repo-name>/'`
   - For user/org pages: `base: '/'`
2. Build with backend URL:

```bash
cd frontend
VITE_API_BASE_URL=https://<your-space>.hf.space npm run build
```

3. Deploy `frontend/dist` to GitHub Pages (via `gh-pages` branch or GitHub Actions).
4. In GitHub repo settings, enable Pages and select deployed source.

## Notes

- Upload supports PNG and JPG/JPEG; output is returned as PNG base64.
- Current backend is intentionally lightweight and uses SQLite by default (no required Postgres container).
- a simple change to triger gh action