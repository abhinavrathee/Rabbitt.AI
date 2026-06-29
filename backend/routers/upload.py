import io
import os
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address

from services.parser import parse_file
from services.ai import generate_summary
from services.email import send_email

router = APIRouter(tags=["Upload"])

# Reuse the same limiter instance created in main.py
limiter = Limiter(key_func=get_remote_address)

ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
ALLOWED_MIME_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/octet-stream",  # some browsers send this for xlsx
}
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 5))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@router.post(
    "/upload",
    summary="Upload sales file and receive AI summary via email",
    response_description="Confirmation message and summary preview",
    responses={
        200: {"description": "Summary generated and email dispatched"},
        400: {"description": "Invalid file type or oversized file"},
        422: {"description": "Validation error (missing fields, bad email)"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error (AI or email failure)"},
    },
)
@limiter.limit(os.getenv("RATE_LIMIT", "5/minute"))
async def upload_file(
    request: Request,
    file: Annotated[UploadFile, File(description="CSV or XLSX sales data file")],
    email: Annotated[EmailStr, Form(description="Recipient email address")],
):
    """
    Upload a `.csv` or `.xlsx` sales file. The API will:

    1. Parse the file into a structured data summary.
    2. Send the summary to Google Gemini to generate a professional narrative.
    3. Email the narrative to the provided address.

    **Rate limit:** 5 requests per minute per IP.
    """
    # --- Validate file extension ---
    filename = file.filename or ""
    ext = os.path.splitext(filename)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Only .csv and .xlsx are accepted.",
        )

    # --- Read and validate size ---
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    # --- Parse ---
    try:
        data_summary = parse_file(io.BytesIO(contents), ext)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not parse file: {exc}")

    # --- AI summary ---
    try:
        summary = await generate_summary(data_summary)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"AI generation failed: {exc}"
        )

    # --- Send email ---
    try:
        await send_email(recipient=str(email), subject="Your Sales Insight Report", body=summary)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Email delivery failed: {exc}")

    return JSONResponse(
        status_code=200,
        content={
            "message": f"Summary generated and sent to {email}",
            "summary_preview": summary[:300] + ("..." if len(summary) > 300 else ""),
        },
    )
