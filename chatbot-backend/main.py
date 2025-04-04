from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Dict
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import generator
from logger import app_logger
from exceptions import ValidationError, RAGError, DatabaseError, ModelError
from config import settings
from security import SecurityMiddleware, sanitize_input


# Rate Limiter Configuration
limiter = Limiter(key_func=get_remote_address)

# Custom rate limit exceeded handler
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    try:
        current_time = time.time()
        reset_time = exc.reset_time if hasattr(exc, 'reset_time') else current_time + 60
        retry_after = int(reset_time - current_time)
        
        client_ip = request.client.host if request.client else "unknown"
        endpoint = request.url.path
        
        app_logger.debug(f"Handling rate limit: {exc}")

        app_logger.warning(
            f"Rate limit exceeded for IP: {client_ip} on endpoint: {endpoint}. "
            f"Retry after: {retry_after} seconds"
        )
        
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too many requests",
                "detail": "Please try again later",
                "retry_after": retry_after
            },
            headers={
                "Retry-After": str(retry_after)
            }
        )
        
    except Exception as e:
        app_logger.error(f"Error in rate limit handler: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": "Error processing rate limit"
            }
        )


class QueryRequest(BaseModel):
    """
    Request model for the generate endpoint.
    
    Attributes:
        question (str): The question to be answered by the RAG system
    """
    question: str = Field(
        ..., 
        min_length=1, 
        max_length=settings.MAX_QUESTION_LENGTH, 
        description="The question to be answered"
    )


class QuestionRequest(BaseModel):
    """
    Request model for the chat endpoint.
    
    Attributes:
        question (str): The question to be answered from predefined responses
    """
    question: str = Field(
        ..., 
        min_length=1, 
        max_length=settings.MAX_QUESTION_LENGTH, 
        description="The question to be answered"
    )


class Response(BaseModel):
    """
    Response model for both endpoints.
    
    Attributes:
        response (str): The generated or retrieved response
    """
    response: str


# Initialize FastAPI with rate limiter
app = FastAPI(
    title="RAG Chatbot API",
    description="A simple RAG (Retrieval-Augmented Generation) chatbot API that provides answers based on stored knowledge and predefined responses.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Add middleware
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SecurityMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    app_logger.info("FastAPI application startup")
    app_logger.info("Rate limiter initialized")
    app_logger.info("SlowAPI middleware initialized")
    app_logger.info("Security middleware initialized")


@app.post("/generate/", response_model=Response, tags=["RAG"])
@limiter.limit(settings.RATE_LIMIT_GENERATE)
async def generate_response(request: Request, query: QueryRequest):
    try:
        app_logger.debug(f"Request from: {request.client.host} - {request.url.path}")
        
        sanitized_question = sanitize_input(query.question)
        app_logger.info(f"Received question: {sanitized_question}")
        
        response = generator.review_chain.invoke(sanitized_question)
        app_logger.info("Successfully generated response")
        return {"response": response}
    except ValueError as e:
        app_logger.error(f"Validation error: {str(e)}")
        raise ValidationError(f"Invalid input: {str(e)}")
    except Exception as e:
        app_logger.error(f"Error generating response: {str(e)}", exc_info=True)
        if "database" in str(e).lower():
            raise DatabaseError("Error accessing the knowledge base")
        elif "model" in str(e).lower():
            raise ModelError("Error with the language model")
        else:
            raise RAGError("Error generating response")


@app.get("/", tags=["Health"])
@limiter.limit(settings.RATE_LIMIT_HEALTH)
async def health_check(request: Request):
    app_logger.info(f"Health check from IP: {request.client.host}")
    return {"message": "Backend is running!"}


responses: Dict[str, str] = {
    "What are the visiting hours at the hospital?": "The hospital is open from 8 AM to 8 PM daily.",
    "Who are the cardiology specialists at Harmony Health Center?": "Dr. John Doe and Dr. Jane Smith are our top cardiology specialists.",
    "What payment options are available at the hospital?": "We accept cash, credit cards, and insurance payments.",
    "How can I book an appointment?": "You can book an appointment by calling our front desk at +1-555-44-44 or visiting our website.",
}


@app.post("/chat/", response_model=Response, tags=["Chat"])
@limiter.limit(settings.RATE_LIMIT_CHAT)
async def generate_response(request: Request, question_request: QuestionRequest):
    try:
        sanitized_question = sanitize_input(question_request.question)
        app_logger.info(f"Received chat question: {sanitized_question}")
        
        question = sanitized_question.strip()
        response_text = responses.get(question, f"I'm not sure about that. Here's some random advice: Stay hydrated and rest well.")
        app_logger.info("Successfully retrieved response")
        return {"response": response_text}
    except ValueError as e:
        app_logger.error(f"Validation error: {str(e)}")
        raise ValidationError(f"Invalid input: {str(e)}")
    except Exception as e:
        app_logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise ValidationError("Error processing request")

