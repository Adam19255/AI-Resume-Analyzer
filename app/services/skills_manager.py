import json
import re
from app.core.config import config

def load_skills():
    """Load skills from the taxonomy file."""
    with open(config.SKILLS_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("required", [])

def save_new_skills(new_skills):
    """Add new skills to the taxonomy if they don't already exist."""
    path = config.SKILLS_FILE_PATH
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"required": []}

    existing = set(data.get("required", []))
    added = [s for s in new_skills if s not in existing]

    if added:
        data["required"].extend(added)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"🧩 Added {len(added)} new skills: {added}")
    else:
        print("No new skills found to add.")

def extract_potential_skills(text):
    """
    Very simple heuristic extractor — in v2 we'll replace this with spaCy NER.
    Detects capitalized or technical words that look like skills.
    """
    candidates = re.findall(r"\b[A-Z][a-zA-Z0-9\+\#]*\b", text)
    # Filter some obvious noise words
    blacklist = {"The", "And", "Or", "In", "Of", "To", "For", "With"}
    cleaned = [c.lower() for c in candidates if c not in blacklist and len(c) > 2]
    return list(set(cleaned))
