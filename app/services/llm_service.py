import os
from openai import OpenAI

def generate_llm_feedback(resume_text: str, job_text: str, missing_skills: list) -> str:
    """
    Generate contextual feedback using OpenAI if an API key exists.
    Falls back gracefully if unavailable.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or OpenAI is None:
        return None  # no key or package, skip AI feedback

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an AI resume reviewer. Given the resume and job description below,
provide specific, personalized improvement feedback.

Resume:
\"\"\"{resume_text[:2000]}\"\"\"

Job Description:
\"\"\"{job_text[:2000]}\"\"\"

Missing skills detected: {', '.join(missing_skills)}

Please:
1. Suggest 3–5 clear improvements to better match the job.
2. Reference relevant skills or job requirements.
3. Use a professional but friendly tone.
4. Be concise (under 200 words).
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional career advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=350
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("⚠️ LLM feedback generation failed:", e)
        # Graceful fallback message for the user
        return (
            "AI feedback is temporarily unavailable "
            "(e.g., quota exceeded or service offline). "
            "Please check your OpenAI plan and try again later."
        )
