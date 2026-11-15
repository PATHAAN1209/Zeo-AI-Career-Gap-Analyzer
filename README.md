# SkillGraph // AI-Powered Career Intelligence & Skill Gap Analysis Platform

> **Tagline:** Scan your skills. Engineer your future.  
> **Theme:** Stark Lab HUD — Futuristic, precise, intelligent, and encouraging sci-fi engineering experience.

---

## 1. Executive Overview

**SkillGraph** is an AI-powered career intelligence web application designed to help students and aspiring engineers determine how prepared they are for industry roles. In three clicks or fewer, candidates can:

1. **Upload their resume (PDF)** or paste raw text.
2. **Select a target career role** (Machine Learning Engineer, Frontend Developer, Data Analyst).
3. **Execute AI-powered skill extraction** and gap classification (`HAVE`, `PARTIAL`, `MISSING`).
4. **View a circular animated Readiness Reactor** score (0–100%) with programmatic scoring.
5. **Inspect holographic skill distributions** via an interactive Recharts radar chart (desktop) or adaptive progress bars (mobile).
6. **Follow a personalized, week-by-week Build Sequence** with interactive milestone check-offs.
7. **Build proposed portfolio projects** mapped directly to critical skill gaps.
8. **Explore curated learning blueprints** across 4 categorized tabs: Videos (YouTube), Books (Google Books / O'Reilly), Courses (Coursera, edX, fast.ai), and Opportunities (Devpost, Unstop, Kaggle, GSoC, LinkedIn).

---

## 2. Technology Stack & Architecture

- **Frontend:**
  - React 18 + Vite
  - Tailwind CSS (Stark Lab HUD design tokens: `#050B14`, `#0B1626`, `#1E3A5F`, `#00E5FF`, `#2979FF`, `#00F5A0`, `#FFC400`, `#FF4D4D`)
  - Recharts (Interactive Radar visualization)
  - Framer Motion & CSS keyframe animations (scanner sweep, pulsing reactor rings)
  - Lucide React icons
  - Canvas Confetti (celebration trigger for 70%+ scores)

- **Backend:**
  - Python 3.12+
  - FastAPI + Uvicorn
  - Pydantic v2 for strict schema validation
  - pdfplumber for primary in-memory PDF extraction with PyMuPDF fallback
  - httpx for concurrent external API resolution
  - python-dotenv for backend secret isolation

- **AI & Scoring:**
  - Configurable LLM provider: Gemini API (`gemini-1.5-flash`), OpenAI API, or high-intelligence semantic rule-based keyword fallback.
  - Zero API key leaks: Keys exist exclusively in backend `.env`.
  - Programmatic scoring: `Have = 1.0`, `Partial = 0.5`, `Missing = 0.0`. Formula: `(Total Points / Total Required) * 100`.

---

## 3. Project Directory Structure

```text
skillgraph/
├── backend/
│   ├── main.py                 # FastAPI application, CORS, static mounting
│   ├── parser.py               # In-memory PDF extraction (pdfplumber + PyMuPDF)
│   ├── analyzer.py             # Skill extraction, semantic matching, roadmap generator
│   ├── scoring.py              # Programmatic readiness scoring & radar coordinates
│   ├── resources.py            # Verified resource engine (Videos, Books, Courses, Opportunities)
│   ├── models.py               # Pydantic request & response schemas
│   ├── roles.json              # Role definitions (ML Engineer, Frontend, Data Analyst)
│   ├── resources.json          # Curated learning resources and active hackathons/fellowships
│   ├── sample_resume.pdf       # Test resume artifact for demo validation
│   ├── requirements.txt        # Backend Python dependencies
│   ├── .env.example            # Environment template
│   └── .env                    # Local environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx          # Futuristic navbar, hexagonal logo, demo triggers
│   │   │   ├── SGCore.jsx          # AI Co-pilot floating widget with pulsing orb
│   │   │   ├── Scanner.jsx         # PDF upload dropzone with laser animation & text fallback
│   │   │   ├── BootTerminal.jsx    # Animated loading terminal with real-time logs
│   │   │   ├── ReactorRing.jsx     # Circular SVG animated readiness score gauge
│   │   │   ├── HoloRadar.jsx       # Recharts radar matrix (desktop) & progress bars (mobile)
│   │   │   ├── StatusModules.jsx   # Skill cards filterable by HAVE / PARTIAL / MISSING
│   │   │   ├── BuildSequence.jsx   # Week-by-week interactive checklist roadmap
│   │   │   ├── ProjectCards.jsx    # Practical portfolio projects addressing gaps
│   │   │   ├── DataCartridges.jsx  # Tabbed learning resources with "START HERE" badge
│   │   │   ├── Missions.jsx        # Verified career opportunities & hackathons
│   │   │   └── ExportModal.jsx     # Dossier print / PDF export modal
│   │   ├── services/
│   │   │   └── api.js              # REST client with automatic fallback
│   │   ├── App.jsx                 # Screen state controller (Landing -> Boot -> Results)
│   │   ├── main.jsx                # React root mount
│   │   └── index.css               # Tailwind + Stark Lab HUD custom classes
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── README.md
└── .gitignore
```

---

## 4. Setup & Execution Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

---

### Step 1: Backend Setup

1. Open a terminal and navigate to `backend/`:
   ```bash
   cd backend
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (optional):
   ```bash
   cp .env.example .env
   ```
   *Note:* If `GEMINI_API_KEY` is omitted, SkillGraph runs in high-performance semantic fallback mode with built-in realistic mock data for zero-downtime hackathon demos.

5. Start the backend server:
   ```bash
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The backend API will be available at: `http://127.0.0.1:8000` (API Docs at `http://127.0.0.1:8000/docs`).

---

### Step 2: Frontend Setup

1. Open a second terminal and navigate to `frontend/`:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The web application will open at: `http://localhost:5173`.

---

### Step 3: All-In-One Unified Production Mode (Optional)

The FastAPI backend automatically serves the pre-built frontend from `frontend/dist`. To run everything through a single port:

```bash
cd frontend && npm run build
cd ../backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000
```
Then visit `http://127.0.0.1:8000` in your web browser!

---

## 5. Endpoints & API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | System health and SG-Core readiness status |
| `GET` | `/roles` | Returns supported career roles and baseline requirements |
| `GET` | `/demo/{role_id}` | Returns instant, pre-computed demonstration dossier |
| `GET` | `/resources/{skill}` | Fetches curated learning resources for a specific skill |
| `POST` | `/analyze` | Multipart upload (PDF file or raw text + role_id) returning complete dossier |

---

## 6. Hackathon Demo Features

1. **One-Click Demo Resumes:** Click the "DEMO" buttons in the navigation bar or below the dropzone to instantly test `ML Engineer`, `Frontend Developer`, or `Data Analyst` without needing a PDF on hand.
2. **Sample PDF Included:** A pre-generated realistic resume is available at `backend/sample_resume.pdf` for testing true file drag-and-drop.
3. **Interactive Task Check-Offs:** The Build Sequence roadmap lets judges check off tasks interactively in real time.
4. **Print / Export Dossier:** Use the "Export Dossier" button in the results view to print or save a clean report via browser print.
5. **Mobile Responsive:** Down to 375px viewport with adaptive horizontal progress bars.
