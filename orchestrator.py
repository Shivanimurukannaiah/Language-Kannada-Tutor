# orchestrator.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from agents.lesson_agent    import LessonAgent
from agents.flashcard_agent import FlashcardAgent
from agents.translate_agent import TranslateAgent
from agents.quiz_agent      import QuizAgent

app = FastAPI(
    title="Kannada Tutor API",
    description="Learn, visualize, translate, and quiz in Kannada",
    version="0.4.0"
)

# Instantiate agents
lesson_agent    = LessonAgent()
flash_agent     = FlashcardAgent()
translate_agent = TranslateAgent()
quiz_agent      = QuizAgent()

# Request schemas
class FlashcardsRequest(BaseModel):
    words: List[str]
    style: str = "cartoon"

class TranslateRequest(BaseModel):
    text: str

class QuizRequest(BaseModel):
    question: str

# ——— Lesson endpoint ———
@app.get("/lesson/", response_model=List[Dict[str, Any]])
async def get_lesson(theme: str, count: int = 5):
    try:
        return lesson_agent.create_lesson(theme, count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ——— Flashcards endpoint ———
@app.post("/flashcards/", response_model=Dict[str, Any])
async def get_flashcards(req: FlashcardsRequest):
    out: Dict[str, Any] = {}
    for w in req.words:
        try:
            url = flash_agent.create_flashcard(w, req.style)
            out[w] = {"image_url": url}
        except Exception as e:
            out[w] = {"error": str(e)}
    return out

# ——— Translate endpoint ———
@app.post("/translate/", response_model=Dict[str, str])
async def translate_text(req: TranslateRequest):
    try:
        return translate_agent.translate(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ——— Quiz endpoint ———
@app.post("/quiz/", response_model=Dict[str, Any])
async def make_quiz(req: QuizRequest):
    # Generate a multiple-choice quiz or return an error payload
    result = quiz_agent.generate_quiz(req.question)
    if "error" in result:
        # Return error info in 200 so UI can display gracefully
        return result
    if "quiz" not in result:
        raise HTTPException(status_code=500, detail="Unexpected quiz format")
    return result

# ——— Run server ———
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("orchestrator:app", host="0.0.0.0", port=8000, reload=True)
