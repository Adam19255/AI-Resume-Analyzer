# 🧠 AI Resume Analyzer

An intelligent resume analysis system built with **FastAPI**, **Python**, and **OpenAI LLMs**, designed to mimic what real-world HR systems and ATS (Applicant Tracking Systems) do — automatically scan resumes, match them against job descriptions, and generate personalized improvement suggestions.

---

## 🚀 Overview

The **AI Resume Analyzer** helps candidates and recruiters quickly evaluate how well a resume aligns with a job posting.  
It uses both **weighted keyword analysis** and **LLM-based contextual understanding** to score and suggest improvements.

### ✨ Key Features

- 📊 **Weighted Scoring System**  
  Compares resume and job description across four main metrics:

  - _Similarity_: Textual overlap and context relevance
  - _Skill Coverage_: Detection of required technical or soft skills
  - _Keyword Density_: Frequency and distribution of key terms
  - _Section Completeness_: Checks if resume includes required sections (education, skills, experience, etc.)

- 💬 **LLM Feedback (Toggleable)**  
  Generates personalized, natural-language feedback using OpenAI’s GPT models.

- 🧩 **Dynamic Configuration**

  - Adjustable weights with sliders directly in the UI
  - Real-time LLM toggle switch
  - Custom error handling and graceful fallbacks

- ⚡ **Responsive Web Interface**  
  Built with Jinja2 templates, dynamic JavaScript, progress animations, and live metric visualization.

- 📂 **File & Text Support**  
  Accepts resumes via direct text or file upload (`.pdf`, `.docx`).

---

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # (Windows)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a .env file in the project root and add your OpenAI key:

```bash
OPENAI_API_KEY=your_api_key_here
```

### ▶️ Run the App

```bash
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000 in your browser.
