from typing import List, Dict, Any, Tuple
from models import SkillItem, RadarPoint

def calculate_readiness_score(skills: List[SkillItem]) -> Tuple[float, str, str, Dict[str, Any]]:
    """
    Computes readiness score programmatically according to PRD specification:
    Have = 1.0, Partial = 0.5, Missing = 0.
    Readiness Score = (Total Skill Points / Total Required Skills) * 100.
    """
    if not skills:
        return 0.0, "Great starting point. Here is your path.", "0-39%", {}

    total_required = len(skills)
    total_points = sum(s.score_contribution for s in skills)
    raw_score = (total_points / total_required) * 100.0
    score = round(raw_score, 1)

    have_count = sum(1 for s in skills if s.status == "HAVE")
    partial_count = sum(1 for s in skills if s.status == "PARTIAL")
    missing_count = sum(1 for s in skills if s.status == "MISSING")

    if score < 40.0:
        message = "Great starting point. Here is your path."
        bracket = "0–39%"
    elif score < 70.0:
        message = "You are on your way. A few key skills to add."
        bracket = "40–69%"
    elif score < 90.0:
        message = "Almost there. Polish these gaps."
        bracket = "70–89%"
    else:
        message = "Interview-ready. Strengthen with a project."
        bracket = "90–100%"

    stats = {
        "total_skills": total_required,
        "total_points": total_points,
        "have_count": have_count,
        "partial_count": partial_count,
        "missing_count": missing_count,
        "completion_rate": round((have_count + 0.5 * partial_count) / total_required * 100, 1)
    }

    return score, message, bracket, stats

def generate_radar_data(skills: List[SkillItem]) -> List[RadarPoint]:
    """
    Transforms skill items into normalized radar chart coordinates.
    HAVE = 100, PARTIAL = 60, MISSING = 15 (to remain visually legible on radar axes).
    """
    radar_points = []
    for s in skills:
        if s.status == "HAVE":
            user_val = 100.0
        elif s.status == "PARTIAL":
            user_val = 55.0
        else:
            user_val = 15.0

        radar_points.append(
            RadarPoint(
                subject=s.name,
                user_level=user_val,
                required_level=100.0,
                status=s.status
            )
        )
    return radar_points
