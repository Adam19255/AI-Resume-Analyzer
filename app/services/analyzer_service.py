# app/services/analyzer_service.py
from sentence_transformers import SentenceTransformer, util
from app.core.config import config
import spacy
import re

# === Load model for semantic similarity ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Lazy-load spaCy for skill extraction ===
_nlp = None
def _get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model not found. Run: python -m spacy download en_core_web_sm"
            )
    return _nlp


# === Main Analysis Function ===
def analyze_resume(resume_text: str, job_text: str):
    """
    Compare a resume with a job description and return:
    - weighted score
    - missing keywords
    - improvement recommendations
    - breakdown metrics
    - optional LLM feedback (handled elsewhere)
    """

    # === 1. Validation ===
    if len(resume_text.split()) < config.MIN_WORDS_RESUME:
        raise ValueError("Resume text seems too short or unreadable.")
    if len(job_text.split()) < config.MIN_WORDS_JOBDESC:
        raise ValueError("Job description too short for analysis.")

    # === 2. Semantic Similarity ===
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_job = model.encode(job_text, convert_to_tensor=True)
    similarity = float(util.cos_sim(emb_resume, emb_job)[0][0])

    # === 3. Skill Extraction (contextual, no persistence) ===
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    # === 4. Skill Coverage ===
    found_skills = [kw for kw in job_skills if kw in resume_skills]
    missing_skills = [kw for kw in job_skills if kw not in resume_skills]
    coverage = len(found_skills) / len(job_skills) if job_skills else 0

    # === 5. Keyword Density & Section Completeness ===
    density = _keyword_density(resume_text)
    completeness = _section_completeness(resume_text)

    # === 6. Weighted Final Score ===
    w = config.WEIGHTS
    final_score = (
        w["semantic_similarity"] * similarity +
        w["skill_coverage"] * coverage +
        w["keyword_density"] * density +
        w["section_completeness"] * completeness
    ) * 100

    # === 7. Return JSON-compatible dict ===
    return {
        "score": round(final_score, 2),
        "missing_keywords": missing_skills,
        "metrics": {
            "similarity": round(similarity, 3),
            "skill_coverage": round(coverage, 3),
            "keyword_density": round(density, 3),
            "section_completeness": round(completeness, 3)
        },
        "ai_feedback": None
    }

# === Skill Extraction ===
def extract_skills(text, mode="spacy"):
    """
    Extracts skill-like terms using either spaCy (NER) or regex fallback.
    """
    if mode == "spacy":
        nlp = _get_nlp()
        doc = nlp(text)
        candidates = []
        for ent in doc.ents:
            # These entity labels often include software, technologies, and organizations
            if ent.label_ in ["ORG", "PRODUCT", "NORP", "WORK_OF_ART"]:
                candidates.append(ent.text.lower())
        clean = [c for c in candidates if 2 < len(c) < 30 and not re.search(r"\d", c)]
        return sorted(set(clean))

    else:
        # regex fallback if spaCy unavailable
        words = re.findall(r"\b[a-zA-Z0-9\+\#\.]{3,}\b", text)
        words = [w.lower() for w in words if len(w) < 20]
        return sorted(set(words))


# === Keyword Density ===
def _keyword_density(text):
    tokens = re.findall(r"\b\w+\b", text.lower())
    matches = [w for w in tokens if w in config.ACTION_VERBS]
    return len(matches) / len(tokens) if tokens else 0


# === Section Completeness ===
def _section_completeness(text):
    sections = ["experience", "education", "skills", "projects"]
    count = sum(1 for s in sections if s in text.lower())
    return count / len(sections)
