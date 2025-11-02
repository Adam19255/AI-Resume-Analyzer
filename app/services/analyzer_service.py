from sentence_transformers import SentenceTransformer, util
import numpy as np
import json
from app.services.recommender_service import generate_recommendations

# Load embedding model (cache)
model = SentenceTransformer("all-MiniLM-L6-v2")

def analyze_resume(resume_text: str, job_text: str):
    # Compute embeddings
    # Encodes resume and job description into dense vectors (tensors).
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_job = model.encode(job_text, convert_to_tensor=True)
    # Computes cosine similarity (−1 to 1; usually ~0.5–0.9 for related texts).
    sim = float(util.cos_sim(emb_resume, emb_job)[0][0])

    # Simple keyword match
    skills = _load_skills()
    missing = [kw for kw in skills if kw.lower() in job_text.lower() and kw.lower() not in resume_text.lower()]

    score = round(sim * 100, 2)
    recommendations = generate_recommendations(missing)

    return {
        "score": score,
        "missing_keywords": missing,
        "recommendations": recommendations,
        "metrics": {"similarity": round(sim, 3)}
    }

def _load_skills():
    try:
        with open("app/assets/skills_taxonomy.json", "r", encoding="utf-8") as f:
            return json.load(f).get("required", [])
    except Exception:
        return ["python", "pytorch", "tensorflow", "sql", "azure", "docker", "transformers"]
