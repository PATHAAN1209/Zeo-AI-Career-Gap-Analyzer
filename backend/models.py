from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

SkillStatus = Literal["HAVE", "PARTIAL", "MISSING"]

class SkillItem(BaseModel):
    name: str
    status: SkillStatus
    score_contribution: float
    importance: str = "high"
    evidence_or_reason: str
    aliases: List[str] = Field(default_factory=list)

class RoadmapWeek(BaseModel):
    week_number: int
    focus: str
    skills_developed: List[str]
    tasks: List[str]
    recommended_resources: List[str]
    expected_outcome: str

class ProjectRecommendation(BaseModel):
    title: str
    description: str
    skills_covered: List[str]
    suggested_approach: str
    expected_outcome: str
    difficulty: str = "Intermediate"

class VideoResource(BaseModel):
    title: str
    channel: str
    url: str
    thumbnail: str
    cost: str = "Free"
    level: str = "Beginner"
    duration: Optional[str] = None
    start_here: bool = False

class BookResource(BaseModel):
    title: str
    author: str
    url: str
    cover: str
    cost: str = "Paid"
    level: str = "Intermediate"
    start_here: bool = False

class CourseResource(BaseModel):
    title: str
    provider: str
    url: str
    cost: str = "Free Audit"
    level: str = "Beginner"
    start_here: bool = False

class SkillResources(BaseModel):
    skill_name: str
    videos: List[VideoResource] = Field(default_factory=list)
    books: List[BookResource] = Field(default_factory=list)
    courses: List[CourseResource] = Field(default_factory=list)

class OpportunityItem(BaseModel):
    id: str = "opp-1"
    title: str
    type: str = "Career"
    organization: str
    url: str
    description: str
    badge: str = "VERIFIED"
    location: str = "Remote / Global"

class RadarPoint(BaseModel):
    subject: str
    user_level: float
    required_level: float = 100.0
    status: SkillStatus

class AnalysisResponse(BaseModel):
    role_id: str
    role_title: str
    category: str
    readiness_score: float
    score_message: str
    score_bracket: str
    stats: Dict[str, Any]
    skills: List[SkillItem]
    have_skills: List[str]
    partial_skills: List[str]
    missing_skills: List[str]
    radar_data: List[RadarPoint]
    roadmap: List[RoadmapWeek]
    projects: List[ProjectRecommendation]
    resources: Dict[str, SkillResources]
    opportunities: List[OpportunityItem]
    summary_insight: str
    co_pilot_status: str = "Analysis complete. Build sequence locked."

class RoleSkillRequirement(BaseModel):
    name: str
    importance: str
    description: str
    aliases: List[str] = Field(default_factory=list)

class RoleDefinition(BaseModel):
    id: str
    title: str
    category: str
    description: str
    required_skills: List[RoleSkillRequirement]
    optional_skills: List[str]

class RolesListResponse(BaseModel):
    roles: List[RoleDefinition]
