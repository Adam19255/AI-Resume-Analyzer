from dotenv import load_dotenv
load_dotenv()

class Config:
    """
    Central configuration for scoring weights and parameters.
    These can later be loaded from .env or a database.
    """

    # === Weighted scoring parameters ===
    WEIGHTS = {
        "semantic_similarity": 0.4,   # how close resume text is to job text
        "skill_coverage": 0.3,        # how many required skills are found
        "keyword_density": 0.2,       # richness of technical terms / verbs
        "section_completeness": 0.1,  # presence of Experience, Education, etc.
    }

    # === Skill taxonomy file path ===
    SKILLS_FILE_PATH = "app/assets/skills_taxonomy.json"

    # === Text processing parameters ===
    MIN_WORDS_RESUME = 100  # sanity check for too-short resumes
    MIN_WORDS_JOBDESC = 50

    # === Action verbs list (for density metric) ===
    ACTION_VERBS = [
        "developed", "designed", "implemented", "created", "analyzed",
        "managed", "led", "built", "optimized", "deployed", "trained",
        "collaborated", "improved"
    ]

config = Config()
