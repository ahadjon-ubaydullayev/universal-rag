from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import generator 
from fastapi.middleware.cors import CORSMiddleware


class QueryRequest(BaseModel):
    question: str

app = FastAPI()

@app.post("/generate/")
async def generate_response(query: QueryRequest):
    try:
        response = generator.review_chain.invoke(query.question)
        print(response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/")
async def health_check():
    return {"message": "Backend is running!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


class QuestionRequest(BaseModel):
    question: str

responses = {
    "What are the visiting hours at the hospital?": "The hospital is open from 8 AM to 8 PM daily.",
    "Who are the cardiology specialists at Harmony Health Center?": "Dr. John Doe and Dr. Jane Smith are our top cardiology specialists.",
    "What payment options are available at the hospital?": "We accept cash, credit cards, and insurance payments.",
}

@app.post("/chat/")
async def generate_response(request: QuestionRequest):
    question = request.question.strip()
    response_text = responses.get(question, f"I'm not sure about that. Here's some random advice: Stay hydrated and rest well.")
    return {"response": response_text}