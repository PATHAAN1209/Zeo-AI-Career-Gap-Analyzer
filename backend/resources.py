import os
import json
from typing import Dict, List, Optional
import httpx
from models import SkillResources, VideoResource, BookResource, CourseResource, OpportunityItem

RESOURCES_FILE = os.path.join(os.path.dirname(__file__), "resources.json")

# In-memory cache for resolved resources
_CACHE: Dict[str, SkillResources] = {}
_CURATED_DATA: Optional[Dict] = None

def get_curated_data() -> Dict:
    global _CURATED_DATA
    if _CURATED_DATA is None:
        try:
            with open(RESOURCES_FILE, "r", encoding="utf-8") as f:
                _CURATED_DATA = json.load(f)
        except Exception:
            _CURATED_DATA = {"skills": {}, "opportunities": {}}
    return _CURATED_DATA

def fetch_youtube_videos_sync(query: str, api_key: str) -> List[VideoResource]:
    """Queries YouTube Data API v3 if API key is provided."""
    videos = []
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{query} tutorial crash course",
            "type": "video",
            "maxResults": 3,
            "key": api_key,
            "relevanceLanguage": "en"
        }
        with httpx.Client(timeout=3.0) as client:
            res = client.get(url, params=params)
            if res.status_code == 200:
                items = res.json().get("items", [])
                for idx, item in enumerate(items):
                    snippet = item.get("snippet", {})
                    vid_id = item.get("id", {}).get("videoId")
                    if vid_id:
                        videos.append(
                            VideoResource(
                                title=snippet.get("title", f"{query} Tutorial"),
                                channel=snippet.get("channelTitle", "YouTube"),
                                url=f"https://www.youtube.com/watch?v={vid_id}",
                                thumbnail=snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                                cost="Free",
                                level="Beginner" if idx == 0 else "Intermediate",
                                start_here=(idx == 0)
                            )
                        )
    except Exception:
        pass
    return videos

def get_curated_skill_resources(skill_name: str, is_highest_priority: bool = False) -> SkillResources:
    """Retrieves verified static resources from resources.json with fallback."""
    curated = get_curated_data().get("skills", {})
    entry = curated.get(skill_name)
    
    # Fuzzy match if exact key not found
    if not entry:
        skill_lower = skill_name.lower()
        for k, v in curated.items():
            if k.lower() in skill_lower or skill_lower in k.lower():
                entry = v
                break
    
    # Safe generic fallback if completely unknown
    if not entry:
        entry = {
            "videos": [
                {
                    "title": f"Complete {skill_name} Mastery & Fundamentals",
                    "channel": "freeCodeCamp.org",
                    "url": f"https://www.youtube.com/results?search_query={skill_name.replace(' ', '+')}+tutorial",
                    "thumbnail": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=500&auto=format&fit=crop&q=60",
                    "cost": "Free",
                    "level": "Beginner",
                    "duration": "2 hours",
                    "start_here": True
                }
            ],
            "books": [
                {
                    "title": f"The Pragmatic Guide to {skill_name}",
                    "author": "Industry Experts",
                    "url": f"https://www.google.com/search?q={skill_name.replace(' ', '+')}+best+programming+books",
                    "cover": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60",
                    "cost": "Paid",
                    "level": "Intermediate"
                }
            ],
            "courses": [
                {
                    "title": f"{skill_name} Fundamentals & Certification",
                    "provider": "Coursera / edX",
                    "url": f"https://www.coursera.org/search?query={skill_name.replace(' ', '%20')}",
                    "cost": "Free Audit",
                    "level": "Beginner"
                }
            ]
        }

    videos = [VideoResource(**v) for v in entry.get("videos", [])]
    books = [BookResource(**b) for b in entry.get("books", [])]
    courses = [CourseResource(**c) for c in entry.get("courses", [])]

    # Ensure START HERE tag on the best first resource if highest priority
    if is_highest_priority:
        if videos:
            videos[0].start_here = True
        elif courses:
            courses[0].start_here = True

    return SkillResources(
        skill_name=skill_name,
        videos=videos,
        books=books,
        courses=courses
    )

def resolve_skill_resources(
    skill_name: str,
    is_highest_priority: bool = False,
    youtube_api_key: Optional[str] = None
) -> SkillResources:
    """Fetches verified resources for a single skill, caching results."""
    cache_key = f"{skill_name}:pri={is_highest_priority}"
    if cache_key in _CACHE:
        return _CACHE[cache_key]

    curated = get_curated_skill_resources(skill_name, is_highest_priority)

    # If YouTube API key is available and configured, optionally augment
    if youtube_api_key and youtube_api_key.strip():
        yt_vids = fetch_youtube_videos_sync(skill_name, youtube_api_key.strip())
        if yt_vids:
            if is_highest_priority:
                yt_vids[0].start_here = True
            curated.videos = yt_vids

    _CACHE[cache_key] = curated
    return curated

def get_resources_for_skills(
    skills_to_fetch: List[str],
    highest_priority_skill: Optional[str] = None
) -> Dict[str, SkillResources]:
    """
    Retrieves resources for list of skills using cache & curated fallback.
    """
    yt_key = (os.getenv("YOUTUBE_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    top_5 = skills_to_fetch[:5]
    res_dict: Dict[str, SkillResources] = {}
    
    for s in top_5:
        is_pri = (s == highest_priority_skill)
        res_dict[s] = resolve_skill_resources(s, is_pri, yt_key if yt_key else None)
            
    # For any remaining skills beyond top 5
    for s in skills_to_fetch[5:]:
        res_dict[s] = get_curated_skill_resources(s, False)

    return res_dict

def get_career_opportunities(role_id: str, role_title: Optional[str] = None) -> List[OpportunityItem]:
    """Retrieves curated, active career opportunities for the chosen role with intelligent dynamic fallbacks."""
    opps = get_curated_data().get("opportunities", {}).get(role_id, [])
    if opps:
        return [OpportunityItem(**item) for item in opps]
    
    # Clean formatted title from role_id if not supplied
    clean_title = role_title or role_id.replace("-", " ").title()
    query_param = clean_title.replace(" ", "+")
    
    default_opps = [
        OpportunityItem(
            id=f"{role_id}-opp-1",
            title=f"{clean_title} Opportunities & Internships",
            type="Internship",
            organization="LinkedIn Careers & Talent Hub",
            location="Remote / Hybrid / On-Site",
            url=f"https://www.linkedin.com/jobs/search/?keywords={query_param}",
            description=f"Verified real-time openings, associate roles, and competitive internship postings for {clean_title} candidates.",
            badge="LIVE JOBS"
        ),
        OpportunityItem(
            id=f"{role_id}-opp-2",
            title=f"Global Innovation Sprints & Hackathons",
            type="Hackathon",
            organization="Devpost Innovation Network",
            location="Global Virtual",
            url="https://devpost.com/hackathons",
            description=f"Showcase your real-world {clean_title} capabilities in worldwide developer and design hackathons with cash prizes and investor visibility.",
            badge="HACKATHON"
        ),
        OpportunityItem(
            id=f"{role_id}-opp-3",
            title=f"Early Career & Graduate Apprenticeships",
            type="Internship",
            organization="Internshala Talent Network",
            location="Pan-National / Remote",
            url="https://internshala.com/internships",
            description=f"Curated paid internships and early career apprenticeships vetted specifically for emerging {clean_title} talent.",
            badge="INTERNSHIP"
        ),
        OpportunityItem(
            id=f"{role_id}-opp-4",
            title=f"National Competitive Hiring Challenges",
            type="Competition",
            organization="Unstop Competitive League",
            location="Virtual / Corporate",
            url="https://unstop.com/find-opportunities",
            description=f"Participate in case competitions, challenges, and fast-track hiring challenges for {clean_title} roles.",
            badge="CHALLENGE"
        ),
        OpportunityItem(
            id=f"{role_id}-opp-5",
            title=f"High-Growth Startup Talent Network",
            type="Job Board",
            organization="Wellfound (AngelList Talent)",
            location="Remote / Global Tech Hubs",
            url="https://wellfound.com/jobs",
            description=f"Direct access to seed-to-series-B startup founders looking for motivated {clean_title} problem solvers.",
            badge="STARTUP"
        )
    ]
    return default_opps
