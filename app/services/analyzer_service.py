from sentence_transformers import SentenceTransformer, util
import re
import json
from app.services.recommender_service import generate_recommendations
from app.core.config import config

# Load embedding model (cache)
model = SentenceTransformer("all-MiniLM-L6-v2")

def analyze_resume(resume_text: str, job_text: str):
    # === Basic validation ===
    if len(resume_text.split()) < config.MIN_WORDS_RESUME:
        raise ValueError("Resume text seems too short or unreadable.")
    if len(job_text.split()) < config.MIN_WORDS_JOBDESC:
        raise ValueError("Job description too short for analysis.")
    
    # === Semantic similarity ===
    # Encodes resume and job description into dense vectors (tensors).
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_job = model.encode(job_text, convert_to_tensor=True)
    # Computes cosine similarity (−1 to 1; usually ~0.5–0.9 for related texts).
    similarity = float(util.cos_sim(emb_resume, emb_job)[0][0])

    # === Skill coverage ===
    skills = _load_skills()
    job_skills = [kw for kw in skills if kw.lower() in job_text.lower()]
    found_skills = [kw for kw in job_skills if kw.lower() in resume_text.lower()]
    coverage = len(found_skills) / len(job_skills) if job_skills else 0

    missing = [kw for kw in job_skills if kw not in found_skills]

    # === Keyword density ===
    density = _keyword_density(resume_text)

    # === Section completeness ===
    completeness = _section_completeness(resume_text)

    # === Weighted score ===
    weights = config.WEIGHTS
    final_score = (
        weights["semantic_similarity"] * similarity +
        weights["skill_coverage"] * coverage +
        weights["keyword_density"] * density +
        weights["section_completeness"] * completeness
    ) * 100

    recommendations = generate_recommendations(missing)

    return {
        "score": round(final_score, 2),
        "missing_keywords": missing,
        "recommendations": recommendations,
        "metrics": {
            "similarity": round(similarity, 3),
            "skill_coverage": round(coverage, 3),
            "keyword_density": round(density, 3),
            "section_completeness": round(completeness, 3)
        }
    }

def _load_skills():
    try:
        with open(config.SKILLS_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("required", [])
    except Exception as e:
        raise RuntimeError(f"Failed to load skills taxonomy: {e}")

def _keyword_density(text):
    tokens = re.findall(r"\b\w+\b", text.lower())
    matches = [w for w in tokens if w in config.ACTION_VERBS]
    return len(matches) / len(tokens) if tokens else 0

def _section_completeness(text):
    sections = ["experience", "education", "skills", "projects"]
    count = sum(1 for s in sections if s in text.lower())
    return count / len(sections)