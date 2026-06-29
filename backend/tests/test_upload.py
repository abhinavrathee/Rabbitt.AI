"""
tests/test_upload.py — Smoke tests for the /api/upload endpoint.
"""
import io
import pytest
from fastapi.testclient import TestClient

# Minimal stubs so tests work without real API keys
import unittest.mock as mock

# Patch external services before importing app
with (
    mock.patch("services.ai.genai.configure"),
    mock.patch("services.ai.genai.GenerativeModel"),
):
    from main import app

client = TestClient(app, raise_server_exceptions=False)

SAMPLE_CSV = b"""Date,Product_Category,Region,Units_Sold,Unit_Price,Revenue,Status
2026-01-05,Electronics,North,150,1200,180000,Shipped
2026-01-12,Home Appliances,South,45,450,20250,Shipped"""


# ── Helpers ────────────────────────────────────────────────────────────────────

def _upload(file_bytes: bytes, filename: str, email: str):
    return client.post(
        "/api/upload",
        files={"file": (filename, io.BytesIO(file_bytes), "text/csv")},
        data={"email": email},
    )


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@mock.patch("routers.upload.generate_summary", return_value="Great sales quarter!")
@mock.patch("routers.upload.send_email", return_value=None)
def test_upload_valid_csv(mock_email, mock_ai):
    r = _upload(SAMPLE_CSV, "data.csv", "test@example.com")
    assert r.status_code == 200
    body = r.json()
    assert "summary_preview" in body
    assert "test@example.com" in body["message"]


def test_upload_invalid_extension():
    r = _upload(b"data", "data.txt", "test@example.com")
    assert r.status_code == 400


def test_upload_invalid_email():
    r = _upload(SAMPLE_CSV, "data.csv", "not-an-email")
    assert r.status_code == 422


def test_upload_missing_file():
    r = client.post("/api/upload", data={"email": "test@example.com"})
    assert r.status_code == 422
