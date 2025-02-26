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
