from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from gemini_service import get_summary_from_gemini, GeminiServiceError

app = FastAPI()

# --- CORS Middleware ---
# allows the frontend (running on a different port) to communicate with the backend
origins = [
    "http://localhost:5173", # Default Vite dev server port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Models ---
# expected request and response data structures for FastAPI
class SummarizeRequest(BaseModel):
    # \S is a regex for any non-whitespace character.
    text: str = Field(..., pattern=r"\S")

class SummarizeResponse(BaseModel):
    summary: str


# --- API Endpoints ---
@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """
    Accepts text and returns a summary using the Gemini service.
    """
    
    try:
        summary_text = get_summary_from_gemini(request.text)
        return SummarizeResponse(summary=summary_text)
    except GeminiServiceError as e:
        # catches the specific error from the service layer
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        # fallback for any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected internal error occurred:\n{e}")


@app.get("/")
def read_root():
    return {"message": "Summarizer API is running."}
