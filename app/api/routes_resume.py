from fastapi import APIRouter, UploadFile, File, Form
from app.services.parser_service import parse_resume_file
from app.services.analyzer_service import analyze_resume
from app.models.resume_models import AnalysisResponse

router = APIRouter()

# response_model=AnalysisResponse tells FastAPI to validate/shape the output.
@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume_endpoint(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Upload a resume and job description -> receive AI analysis
    """
    # Reads and cleans the uploaded resume (PDF/DOCX → plain text).
    resume_text = await parse_resume_file(resume_file)
    # Runs the core analysis (embeddings similarity + keyword coverage + recommendations).
    result = analyze_resume(resume_text, job_description)
    # Returns a dict that FastAPI validates and serializes according to AnalysisResponse.
    return result
