import os
import json
import re
from typing import Dict, Any, List, Tuple
from models import SkillItem, SkillStatus, RoadmapWeek, ProjectRecommendation

SYSTEM_PROMPT = """You are SG-Core, an elite AI skill auditor and technical career intelligence engine.
Your task is to analyze candidate resume text against the requirements of a specific career role.

Rules:
1. Compare candidate experience, projects, tools, and coursework against every required skill.
2. Classify each required skill strictly into one of:
   - "HAVE": Clear evidence of usage, projects, work experience, or coursework.
   - "PARTIAL": Some familiarity, mentioned in passing, or tangential experience without deep execution.
   - "MISSING": No sufficient evidence found.
3. Be rigorous: Do NOT assume a skill exists simply because it appears in a casual project title without supporting context.
4. Generate a tailored week-by-week learning roadmap (4 to 6 weeks) prioritizing missing and partial skills.
5. Generate 2 to 3 practical, resume-worthy portfolio projects directly addressing the critical skill gaps.
6. Provide a concise technical executive summary insight (1-2 sentences) from SG-Core.
7. Return strictly valid JSON adhering to the specified schema. No markdown formatting, no preambles.
"""

def get_role_definition(roles_data: Dict, role_id: str) -> Dict:
    for r in roles_data.get("roles", []):
        if r["id"] == role_id:
            return r
    raise ValueError(f"Role '{role_id}' not found in role catalog.")

def fallback_semantic_analyzer(resume_text: str, role: Dict) -> Tuple[List[SkillItem], List[RoadmapWeek], List[ProjectRecommendation], str]:
    """
    Intelligent semantic and keyword rule-based analyzer when no LLM API key is supplied or external LLM fails.
    Accurately examines context, frequency, and depth in resume text.
    """
    resume_lower = resume_text.lower()
    classified_skills: List[SkillItem] = []
    
    missing_skill_names: List[str] = []
    partial_skill_names: List[str] = []
    have_skill_names: List[str] = []

    for req in role.get("required_skills", []):
        skill_name = req["name"]
        aliases = [a.lower() for a in req.get("aliases", [])] + [skill_name.lower()]
        
        total_hits = 0
        strong_evidence = False
        evidence_snippet = ""
        
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            matches = list(re.finditer(pattern, resume_lower))
            if matches:
                total_hits += len(matches)
                first_match = matches[0]
                start = max(0, first_match.start() - 40)
                end = min(len(resume_text), first_match.end() + 60)
                snip = resume_text[start:end].replace('\n', ' ').strip()
                if not evidence_snippet:
                    evidence_snippet = f"...{snip}..."
                    
                window_start = max(0, first_match.start() - 100)
                window_end = min(len(resume_lower), first_match.end() + 100)
                window_text = resume_lower[window_start:window_end]
                if any(w in window_text for w in ["built", "developed", "implemented", "deployed", "designed", "engineered", "pipeline", "model", "project", "architecture", "lead", "optimized"]):
                    strong_evidence = True

        if total_hits >= 2 or strong_evidence:
            status: SkillStatus = "HAVE"
            score = 1.0
            reason = f"Demonstrated in resume with practical context ({total_hits} mention{'s' if total_hits > 1 else ''}). {evidence_snippet}"
            have_skill_names.append(skill_name)
        elif total_hits == 1:
            status: SkillStatus = "PARTIAL"
            score = 0.5
            reason = f"Mentioned in resume, but limited production evidence or project depth identified. {evidence_snippet}"
            partial_skill_names.append(skill_name)
        else:
            status: SkillStatus = "MISSING"
            score = 0.0
            reason = f"No sufficient evidence or project application found in candidate resume."
            missing_skill_names.append(skill_name)

        classified_skills.append(
            SkillItem(
                name=skill_name,
                status=status,
                score_contribution=score,
                importance=req.get("importance", "high"),
                evidence_or_reason=reason,
                aliases=req.get("aliases", [])
            )
        )

    # Generate personalized week-by-week roadmap prioritizing missing, then partial
    prioritized_gaps = missing_skill_names + partial_skill_names
    if not prioritized_gaps:
        prioritized_gaps = [req["name"] for req in role.get("required_skills", [])[-2:]]

    roadmap: List[RoadmapWeek] = []
    week_num = 1
    
    for i in range(0, min(len(prioritized_gaps), 6), 2):
        pair = prioritized_gaps[i:i+2]
        skill_str = " & ".join(pair)
        
        roadmap.append(
            RoadmapWeek(
                week_number=week_num,
                focus=f"Core Foundations & Implementation: {skill_str}",
                skills_developed=pair,
                tasks=[
                    f"Study architectural concepts and patterns for {pair[0]}.",
                    f"Complete 3 hands-on laboratory exercises focusing on real-world constraints.",
                    f"Build an end-to-end prototype integrating {skill_str} with automated tests."
                ],
                recommended_resources=[
                    f"Interactive documentation and community blueprints for {pair[0]}.",
                    f"Guided benchmark repo demonstrating standard industry workflows."
                ],
                expected_outcome=f"Working standalone module verifying functional competency in {skill_str}."
            )
        )
        week_num += 1

    while week_num <= 4:
        roadmap.append(
            RoadmapWeek(
                week_number=week_num,
                focus=f"Systems Integration & Production Hardening",
                skills_developed=prioritized_gaps[:2] if prioritized_gaps else ["System Architecture"],
                tasks=[
                    "Conduct end-to-end integration testing and benchmark latency/metrics.",
                    "Package the build with containerization, CI/CD, and monitoring telemetry.",
                    "Publish a technical writeup and showcase repository on GitHub."
                ],
                recommended_resources=["Production deployment best practices guide", "Automated test suite templates"],
                expected_outcome="Full production-ready portfolio piece with public documentation."
            )
        )
        week_num += 1

    # Practical portfolio project recommendations
    projects: List[ProjectRecommendation] = []
    role_id = role["id"]
    
    if role_id == "ml-engineer":
        projects = [
            ProjectRecommendation(
                title="End-to-End Multimodal Semantic Search Engine",
                description="Engineered a microservice that generates and indexes vector embeddings from text and imagery, serving sub-100ms similarity queries.",
                skills_covered=["Deep Learning (PyTorch or TensorFlow)", "Computer Vision or NLP", "MLOps & Model Deployment"],
                suggested_approach="Use Hugging Face CLIP / Sentence-Transformers, Qdrant/Chroma vector DB, containerize with Docker, and expose a FastAPI endpoint with rate limiting.",
                expected_outcome="Deployed live demo on Hugging Face Spaces or Railway with public API documentation.",
                difficulty="Advanced"
            ),
            ProjectRecommendation(
                title="Production Predictive Pipeline with MLflow & Automated Retraining",
                description="Built an enterprise feature store and automated retraining pipeline with continuous drift monitoring and model registry validation.",
                skills_covered=["Scikit-Learn", "Data Preprocessing & Feature Engineering", "Model Evaluation & Validation"],
                suggested_approach="Ingest live stream data, compute rolling feature aggregates with Pandas, evaluate ROC-AUC/F1 thresholds, and log metrics to MLflow.",
                expected_outcome="Interactive Streamlit dashboard displaying live model telemetry and drift alerts.",
                difficulty="Intermediate"
            )
        ]
    elif role_id == "frontend-dev":
        projects = [
            ProjectRecommendation(
                title="Enterprise Real-Time Collaborative Canvas",
                description="Engineered a low-latency collaborative state management application featuring responsive layouts, custom hooks, and WebSocket synchronization.",
                skills_covered=["React.js", "TypeScript", "State Management", "Responsive & Mobile-First Design"],
                suggested_approach="Build with React 19, TypeScript, Zustand, and Tailwind CSS; implement optimistic UI updates, conflict resolution, and keyboard shortcuts.",
                expected_outcome="Lighthouse 98+ performance score, WCAG 2.1 AA accessibility compliance, and live Vercel deployment.",
                difficulty="Intermediate"
            ),
            ProjectRecommendation(
                title="Modular Design System & Headless Component Library",
                description="Architected a reusable, accessible component library published to npm, with zero layout shift and dark/holographic theme tokens.",
                skills_covered=["HTML5 & Semantic Web", "CSS3, Flexbox & Grid", "Modern JavaScript (ES6+)", "TypeScript"],
                suggested_approach="Create polymorphic components with Radix UI primitives and Tailwind CSS, documented with interactive Storybook stories.",
                expected_outcome="Complete npm package with typed exports and Storybook playground.",
                difficulty="Advanced"
            )
        ]
    else: # data-analyst
        projects = [
            ProjectRecommendation(
                title="SaaS Revenue Retention & Cohort Churn Intelligence Dashboard",
                description="Designed an executive BI suite mapping customer lifetime value (LTV), cohort survival curves, and subscription revenue drivers.",
                skills_covered=["SQL & Relational Databases", "Business Intelligence Tools", "Exploratory Data Analysis (EDA)"],
                suggested_approach="Write multi-tier CTEs and window functions in PostgreSQL, ingest into Tableau/Power BI, and design interactive drill-down filters.",
                expected_outcome="Polished public Tableau Public dashboard with documented business insights and executive deck.",
                difficulty="Intermediate"
            ),
            ProjectRecommendation(
                title="Algorithmic Customer Segmentation & Statistical Anomaly Detector",
                description="Built an end-to-end data cleaning, hypothesis testing, and RFM behavioral clustering engine for ecommerce transaction streams.",
                skills_covered=["Python for Data Analysis", "Statistical Analysis & Hypothesis Testing", "Data Cleaning & Transformation", "Data Visualization"],
                suggested_approach="Clean noisy transaction logs with Pandas, run two-sample t-tests and ANOVA on conversion variations, and plot distributions with Seaborn.",
                expected_outcome="Jupyter notebook published on Kaggle/GitHub with interactive visualizations and clean reproducible pipeline.",
                difficulty="Intermediate"
            )
        ]

    num_have = len(have_skill_names)
    num_total = len(classified_skills)
    summary_insight = (
        f"SG-Core detected strong foundations in {', '.join(have_skill_names[:3]) if have_skill_names else 'general programming'} "
        f"({num_have}/{num_total} core requirements met). "
        f"Prioritizing {' and '.join(missing_skill_names[:2]) if missing_skill_names else 'production hardening'} "
        f"will accelerate qualification for mid-level {role['title']} evaluation benchmarks."
    )

    return classified_skills, roadmap, projects, summary_insight

def analyze_skills(resume_text: str, role: Dict) -> Tuple[List[SkillItem], List[RoadmapWeek], List[ProjectRecommendation], str]:
    """
    Skill extraction and analysis pipeline. Uses Gemini if valid key provided, otherwise semantic analyzer.
    """
    gemini_key = (os.getenv("GEMINI_API_KEY") or "").strip()
    openai_key = (os.getenv("OPENAI_API_KEY") or "").strip()

    if not gemini_key and not openai_key:
        return fallback_semantic_analyzer(resume_text, role)

    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
Role Requirements:
Title: {role['title']}
Required Skills: {json.dumps([s['name'] for s in role['required_skills']])}

Candidate Resume Text:
\"\"\"
{resume_text[:4000]}
\"\"\"

Respond with JSON adhering to this exact schema:
{{
  "skills": [
    {{
      "name": "<Skill Name>",
      "status": "HAVE" | "PARTIAL" | "MISSING",
      "score_contribution": 1.0 | 0.5 | 0.0,
      "evidence_or_reason": "<1-2 sentence evidence or gap reason>"
    }}
  ],
  "roadmap": [
    {{
      "week_number": 1,
      "focus": "<Focus Topic>",
      "skills_developed": ["<Skill 1>"],
      "tasks": ["<Task 1>", "<Task 2>"],
      "recommended_resources": ["<Resource 1>"],
      "expected_outcome": "<Outcome>"
    }}
  ],
  "projects": [
    {{
      "title": "<Project Title>",
      "description": "<Description>",
      "skills_covered": ["<Skill>"],
      "suggested_approach": "<Approach>",
      "expected_outcome": "<Outcome>",
      "difficulty": "Intermediate"
    }}
  ],
  "summary_insight": "<1-2 sentences technical summary>"
}}
"""
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            skills = [SkillItem(**s) for s in data.get("skills", [])]
            roadmap = [RoadmapWeek(**w) for w in data.get("roadmap", [])]
            projects = [ProjectRecommendation(**p) for p in data.get("projects", [])]
            summary_insight = data.get("summary_insight", "Analysis compiled by SG-Core.")
            
            req_names = {r["name"] for r in role["required_skills"]}
            extracted_names = {s.name for s in skills}
            if req_names.issubset(extracted_names) and skills:
                return skills, roadmap, projects, summary_insight
        except Exception:
            pass

    return fallback_semantic_analyzer(resume_text, role)
