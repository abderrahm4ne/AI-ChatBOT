
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from service.stream_service import get_chat_stream
from agent import create_my_agent
import agent

import os, shutil

UPLOAD_DIR = "./assets"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="RAG AIChatBOT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    thread_id: str

class AnswerMessage(BaseModel):
    answer: str


### Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return{
        "messages": "It's pulsing"
    }

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request:
        raise HTTPException(status_code=404, detail="no request provided")
    
    try:
        return StreamingResponse(
            get_chat_stream(
                message=request.prompt,
                thread_id=request.thread_id,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-pdf")
async def upload_def(file: UploadFile):
    if not file:
        raise HTTPException(status_code=404, detail="no file uploaded")
    
    file_name = file.filename
    if not file_name or not file_name.endswith('.pdf'):
        raise HTTPException(status_code=401, detail="the file must be pdf")
    
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        agent.current_agent = create_my_agent(file_path)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        await file.close()
