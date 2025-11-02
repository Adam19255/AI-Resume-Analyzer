import os
from openai import OpenAI
from typing import List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_llm_feedback(resume_text: str, job_text: str, missing_skills: List[str]) -> str:
    prompt = f"""
You are an AI resume reviewer.
Given the following resume and job description, provide specific improvement advice.

Resume:
\"\"\"{resume_text[:2000]}\"\"\"

Job Description:
\"\"\"{job_text[:2000]}\"\"\"

Missing skills detected: {', '.join(missing_skills)}

Please:
1. Suggest 3–5 concrete improvements or rewrites.
2. Reference relevant skills or job requirements.
3. Use a friendly, professional tone.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional career advisor and resume coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=350
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("⚠️ LLM feedback generation failed:", e)
        return "Could not generate AI feedback. Please try again later."
