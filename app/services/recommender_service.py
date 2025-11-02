def generate_recommendations(missing_keywords):
    recs = []
    for kw in missing_keywords:
        recs.append(f"Consider adding experience with **{kw}** — it appears in the job posting but not in your resume.")
    if not recs:
        recs.append("Your resume covers most of the required terms — great alignment!")
    return recs
