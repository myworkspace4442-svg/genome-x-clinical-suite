# Genome-X Suite: Clinical-Grade AMR Engine & Structural Viewer

Genome-X Suite is an enterprise-grade bioinformatics and machine learning platform designed for antimicrobial resistance (AMR) prediction, sequence alignment, and real-time 3D protein structure analysis.

The system utilizes a decoupled architecture featuring a Python FastAPI backend for dual-stream ML inference and a React + TypeScript frontend integrated with Mol* for dynamic, two-way synchronized structural visualization.

---

## Key System Features

### 1. High-Performance Machine Learning & XAI
* **Dual-Stream odes.

### 4. Clinical Audit Trail
* **Prediction Logs:** Retains historical inference records with export options (CSV) for regulatory compliance.

---

## Design System Architecture

The user interface follows strict UI/UX design standards:

* **8pt Grid System:** All paddings, margins, and layout gaps adhere to multiples of 8px (4px, 8px, 16px, 24px, 32px).
* **60-30-10 Color Rule:**
  * 60% Neutral Background: Light Slate (`#F9FAFB` / `#FFFFFF`)
  * 30% Text & Borders: Dark Slate (`#1F2937`) & Crisp Gray (`#E5E7EB`)
  * 10% Accent Action: Brand Blue (`#2563EB`)
* **Typography Scale:**
  * Page Headers: 24px Bold (32px line height)
  * Section Titles: 18px Semi-Bold (24px line height)
  * Body Text: 14px Regular (20px line height)
  * Captions & Muted Text: 12px Regular (`#6B7280`)

---

## Project Directory Structure

```text
genome-x-suite/
├── app/                          # FastAPI Backend Engine
│   ├── main_api.py               # REST API Routes & Endpoints
│   ├── database.py               # SQLite Persistence Layer
│   └── models/                   # 1D-CNN + XGBoost ML Pipeline
│
├── genome-x-frontend/            # React + TypeScript Frontend
│   ├── src/
│   │   ├── components/           # UI Components
│   │   │   ├── SequenceAlignmentCanvas.tsx
│   │   │   ├── Molstar3DViewer.tsx
│   │   │   └── GenomeTrackBrowser.tsx
│   │   ├── store/
│   │   │   └── useGenomeStore.ts # Zustand State Management (Cross-Highlighting)
│   │   ├── services/
│   │   │   └── api.ts            # Axios Client for FastAPI
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tsconfig.json
│
└── Dockerfile                    # Containerization Spec