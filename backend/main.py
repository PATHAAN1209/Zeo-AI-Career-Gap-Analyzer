import os
import json
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from models import (
    RolesListResponse,
    RoleDefinition,
    AnalysisResponse,
    SkillResources
)
from parser import (
    validate_pdf_file,
    extract_text_from_pdf_bytes,
    PDFExtractionError
)
from scoring import (
    calculate_readiness_score,
    generate_radar_data
)
from analyzer import (
    get_role_definition,
    analyze_skills,
    fallback_semantic_analyzer
)
from resources import (
    get_resources_for_skills,
    get_curated_skill_resources,
    get_career_opportunities,
    resolve_skill_resources
)

ROLES_FILE = os.path.join(os.path.dirname(__file__), "roles.json")

app = FastAPI(
    title="SkillGraph API",
    description="Scan your skills. Engineer your future. AI-Powered Career Intelligence & Skill Gap Analysis Platform.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_roles_catalog() -> dict:
    with open(ROLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "system": "SkillGraph SG-Core Subsystem",
        "version": "1.0.0",
        "llm_configured": bool((os.getenv("GEMINI_API_KEY") or "").strip() or (os.getenv("OPENAI_API_KEY") or "").strip())
    }

@app.get("/roles", response_model=RolesListResponse)
def get_roles():
    catalog = load_roles_catalog()
    return RolesListResponse(
        roles=[RoleDefinition(**r) for r in catalog.get("roles", [])]
    )

@app.get("/resources/{skill_name}", response_model=SkillResources)
def get_skill_resources(skill_name: str):
    res = resolve_skill_resources(skill_name, is_highest_priority=False)
    return res

@app.get("/demo/{role_id}", response_model=AnalysisResponse)
def get_demo_analysis(role_id: str):
    """
    Returns an instant, cached, high-fidelity sample analysis for hackathon demonstrations.
    """
    catalog = load_roles_catalog()
    try:
        role = get_role_definition(catalog, role_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Role '{role_id}' not found.")

    sample_resumes = {
        "ml-engineer": """
Arjun Patel - Junior Software & ML Developer
Education: B.Tech in Computer Science, 2024
Skills: Python, Scikit-Learn, Pandas, NumPy, Data Preprocessing, Feature Engineering, Git.
Experience:
- Built customer churn prediction model using Random Forest and XGBoost in Scikit-Learn with 89% ROC-AUC.
- Cleaned and prepared tabular datasets with missing value imputation and one-hot encoding.
- Developed simple Flask REST endpoints for model inference.
Projects:
- House Price Regression with Scikit-learn and exploratory data analysis.
- Basic Linear Algebra and Multivariate Calculus coursework projects.
""",
        "frontend-dev": """
Maya Lin - Web Developer Intern
Education: B.S. Software Engineering, 2024
Technical Skills: JavaScript (ES6+), React.js, HTML5, CSS3, Flexbox & Grid, Responsive Design, REST APIs, Tailwind CSS.
Experience:
- Developed responsive web interfaces for student portal using React.js and CSS Grid.
- Integrated third-party REST APIs using Axios and standard Fetch API with loading and error states.
- Re-architected mobile layouts to ensure 100% mobile-first viewport compatibility.
Projects:
- E-commerce catalog built in React with shopping cart state using Context API.
- Semantic HTML and accessibility audit project adhering to WCAG 2.1 guidelines.
""",
        "data-analyst": """
Rohan Sharma - Associate Data Analyst
Education: B.S. Statistics & Economics, 2024
Core Competencies: SQL (PostgreSQL, MySQL), Excel (VLOOKUP, Pivot Tables, Power Query), Python (Pandas, Matplotlib), EDA.
Experience:
- Analyzed marketing campaign conversion rates writing complex SQL queries with CTEs and multi-table joins.
- Designed automated Excel financial reporting templates with pivot tables and dynamic dashboard charts.
- Conducted exploratory data analysis (EDA) on 200,000+ consumer records identifying key purchase trends.
Projects:
- Regional Sales Performance Dashboard designed in Tableau Public.
- Data Cleaning script in Pandas handling outliers, duplicates, and type mismatches.
"""
    }

    text = sample_resumes.get(role_id, sample_resumes["ml-engineer"])
    return execute_analysis(text, role)

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    role_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None)
):
    catalog = load_roles_catalog()
    try:
        role = get_role_definition(catalog, role_id)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid career role selected: '{role_id}'.")

    extracted_text = ""

    if file is not None and file.filename:
        try:
            file_bytes = await file.read()
            validate_pdf_file(file.filename, file_bytes)
            extracted_text, method = extract_text_from_pdf_bytes(file_bytes)
        except PDFExtractionError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error processing PDF file: {str(e)}")

    elif resume_text and resume_text.strip():
        extracted_text = resume_text.strip()
        if len(extracted_text) < 40:
            raise HTTPException(
                status_code=400,
                detail="Provided resume text is too short to perform a meaningful skill gap analysis."
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide a PDF resume file or paste your resume text."
        )

    return execute_analysis(extracted_text, role)

def execute_analysis(resume_text: str, role: dict) -> AnalysisResponse:
    # 1. Run AI / Semantic Skill Analysis
    skills, roadmap, projects, summary_insight = analyze_skills(resume_text, role)

    # 2. Programmatic Readiness Score & Stats calculation
    score, score_msg, score_bracket, stats = calculate_readiness_score(skills)

    # 3. Radar data transformation
    radar_data = generate_radar_data(skills)

    # 4. Group skills by status
    have_skills = [s.name for s in skills if s.status == "HAVE"]
    partial_skills = [s.name for s in skills if s.status == "PARTIAL"]
    missing_skills = [s.name for s in skills if s.status == "MISSING"]

    # 5. Determine highest priority gap for "START HERE" badge
    highest_priority = missing_skills[0] if missing_skills else (partial_skills[0] if partial_skills else None)

    # 6. Retrieve verified learning resources
    gaps_to_fetch = missing_skills + partial_skills
    if not gaps_to_fetch:
        gaps_to_fetch = [s.name for s in skills]

    resources_map = get_resources_for_skills(gaps_to_fetch, highest_priority_skill=highest_priority)

    # 7. Retrieve curated opportunities
    opportunities = get_career_opportunities(role["id"], role.get("title"))

    return AnalysisResponse(
        role_id=role["id"],
        role_title=role["title"],
        category=role["category"],
        readiness_score=score,
        score_message=score_msg,
        score_bracket=score_bracket,
        stats=stats,
        skills=skills,
        have_skills=have_skills,
        partial_skills=partial_skills,
        missing_skills=missing_skills,
        radar_data=radar_data,
        roadmap=roadmap,
        projects=projects,
        resources=resources_map,
        opportunities=opportunities,
        summary_insight=summary_insight,
        co_pilot_status="Telemetry synced. Mission parameters locked."
    )

# Mount frontend production build if available
FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(FRONTEND_DIST):
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, RedirectResponse

    @app.get("/")
    def serve_frontend_root():
        index_file = os.path.join(FRONTEND_DIST, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "SkillGraph API is online. Build frontend to see UI."}

    @app.get("/analyze")
    @app.get("/analyze/")
    def analyze_get_redirect():
        return RedirectResponse(url="/")

    # Mount static assets directory
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
