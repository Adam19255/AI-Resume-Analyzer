from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes_resume import router as resume_router
from app.core.error_handlers import register_error_handlers

app = FastAPI(
    title="AI Resume Analyzer",
    description="An AI-powered API that analyzes resumes vs job descriptions and returns improvement suggestions.",
    version="1.0.0",
)

register_error_handlers(app)

# Allow cross-origin access (for future React / Streamlit frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(resume_router, prefix="/api/v1/resume", tags=["Resume Analysis"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI Resume Analyzer API 🚀"}
