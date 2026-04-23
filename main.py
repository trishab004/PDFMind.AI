from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import groq
import os
import io

app = FastAPI(title="PDFMind.AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store extracted PDF text in memory (per-session use)
# For multi-user production, use Redis or a DB
pdf_store: dict[str, str] = {}

client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"  # Free, fast, generous limits. Alternatives: mixtral-8x7b-32768, gemma2-9b-it


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def ask_groq(system_prompt: str, user_message: str) -> str:
    """Send a message to Groq and return the response."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=1024,
        temperature=0.3,
    )
    return response.choices[0].message.content


# ── Routes ────────────────────────────────────────────────────────────────────

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF and extract its text. Returns a session_id to use in /summarize and /ask."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()
    text = extract_text_from_pdf(contents)

    if not text:
        raise HTTPException(status_code=422, detail="Could not extract text from this PDF. It may be scanned/image-based.")

    # Use filename as a simple session key (add UUID for production)
    session_id = file.filename.replace(" ", "_")
    pdf_store[session_id] = text

    return {"session_id": session_id, "page_count": text.count("\n"), "message": "PDF uploaded successfully."}


@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    """Upload and summarize a PDF in one step."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()
    text = extract_text_from_pdf(contents)

    if not text:
        raise HTTPException(status_code=422, detail="Could not extract text from this PDF.")

    session_id = file.filename.replace(" ", "_")
    pdf_store[session_id] = text

    # Truncate to ~12000 chars to stay within token limits
    truncated = text[:12000]

    summary = ask_groq(
        system_prompt="You are a helpful assistant that summarizes documents clearly and concisely.",
        user_message=f"Please summarize the following document. Highlight the main topics, key points, and any important conclusions:\n\n{truncated}"
    )

    return {"session_id": session_id, "summary": summary}


class AskRequest(BaseModel):
    session_id: str
    question: str


@app.post("/ask")
async def ask_question(body: AskRequest):
    """Ask a question about a previously uploaded PDF."""
    text = pdf_store.get(body.session_id)
    if not text:
        raise HTTPException(status_code=404, detail="Session not found. Please upload your PDF again.")

    truncated = text[:12000]

    answer = ask_groq(
        system_prompt=(
            "You are a helpful assistant answering questions about a document. "
            "Only use information from the document provided. "
            "If the answer is not in the document, say so clearly.\n\n"
            f"DOCUMENT:\n{truncated}"
        ),
        user_message=body.question,
    )

    return {"answer": answer}


@app.get("/")
def root():
    # Serve the frontend interface directly from the backend
    return FileResponse("index.html")


