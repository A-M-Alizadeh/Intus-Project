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

## Analyze endpoint (feature/organ-detection)

- New endpoint: `POST /api/imaging/analyze/`
- Input: multipart form-data with `image`
- Output:

```json
{
  "detected": true,
  "confidence": 0.87,
  "bounding_box": {
    "x": 120,
    "y": 95,
    "width": 310,
    "height": 280
  }
}
```

The detection logic uses a simple OpenCV threshold + largest contour heuristic (no deep learning), as required by the task. This is a heuristic method based only on grayscale intensity thresholding, morphological cleanup, and selecting the largest external contour as the ROI. Because it does not learn organ-specific features, it may not detect organs with high accuracy and can produce overconfident scores for non-target images; it mainly considers contour size/shape and pixel distribution after thresholding. If robust, clinically meaningful detection is needed, use a trained ML/DL pipeline (for example, a validated classifier or segmentation model such as CNN/U-Net) with proper dataset coverage, calibration, and evaluation metrics.

Current heuristic confidence is computed as:

`confidence = clamp(contour_area / image_area, 0, 1)`

where:
- `contour_area` = area of the largest detected contour
- `image_area` = total image pixels (`height * width`)

Returned confidence is rounded to 2 decimals.

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
2. In the Space repo, use the root `Dockerfile` from this repository.
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
- Push a small change to trigger the GitHub Actions deploy.

## Branches and live URLs

### main (original submission)
- Frontend URL: `https://a-m-alizadeh.github.io/Intus-Project/`
- Backend URL: `https://ali-alizadeh-intus-project.hf.space/`

### feature/organ-detection (new task)
- Frontend URL: `ADD_FEATURE_FRONTEND_URL_HERE`
- Backend URL: `ADD_FEATURE_BACKEND_URL_HERE`