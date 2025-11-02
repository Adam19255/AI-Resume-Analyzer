from fastapi import FastAPI, Request, Form, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from markupsafe import Markup
import markdown

# Internal imports
from app.api.routes_resume import router as resume_router
from app.core.error_handlers import register_error_handlers
from app.core.config import config
from app.services.analyzer_service import analyze_resume
from app.services.parser_service import parse_resume_file

# ------------------------------------------------------------------
# FastAPI app configuration
# ------------------------------------------------------------------
app = FastAPI(title="AI Resume Analyzer")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

register_error_handlers(app)

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# API routes
# ------------------------------------------------------------------
app.include_router(resume_router, prefix="/api/v1/resume", tags=["Resume Analysis"])

# ------------------------------------------------------------------
# Web UI routes
# ------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Show homepage form."""
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, resume: str = Form(...), job: str = Form(...)):
    """Handle text submission for resume analysis."""
    try:
        result = analyze_resume(resume, job)
        if "ai_feedback" in result and result["ai_feedback"]:
            result["ai_feedback"] = Markup(markdown.markdown(result["ai_feedback"]))
    except Exception as e:
        result = {"error": str(e)}
    return templates.TemplateResponse("index.html", {"request": request, "result": result})


@app.post("/upload", response_class=HTMLResponse)
async def upload_resume(
    request: Request,
    resume_file: UploadFile = File(...),
    job: str = Form(...)
):
    """Handle file upload (PDF/DOCX) + job description."""
    try:
        resume_text = await parse_resume_file(resume_file)
        result = analyze_resume(resume_text, job)
        if "ai_feedback" in result and result["ai_feedback"]:
            result["ai_feedback"] = Markup(markdown.markdown(result["ai_feedback"]))
    except ValueError as e:
        result = {"error": str(e)}
    except Exception as e:
        result = {"error": f"Unexpected error: {str(e)}"}

    return templates.TemplateResponse("index.html", {"request": request, "result": result})


# ------------------------------------------------------------------
# LLM Feedback Toggle
# ------------------------------------------------------------------
@app.post("/toggle_llm")
async def toggle_llm():
    """Toggle the LLM feedback setting."""
    config.USE_LLM_FEEDBACK = not config.USE_LLM_FEEDBACK
    return JSONResponse({"status": "ok", "USE_LLM_FEEDBACK": config.USE_LLM_FEEDBACK})


# ------------------------------------------------------------------
# Update Weights Endpoint
# ------------------------------------------------------------------
@app.post("/update_weights")
async def update_weights(weights: dict = Body(...)):
    """Update scoring weights dynamically."""
    config.WEIGHTS.update(weights)
    return {"status": "ok", "weights": config.WEIGHTS}
