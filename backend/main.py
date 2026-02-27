from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from service.stream_service import get_chat_stream
import agent

import os

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
        # enriched_message = f"{request.prompt}\n\nthink and search with the pdf_tool and take your time"
        result = agent.current_agent.invoke(
            input={"messages": [{"role": "user", "content": request.prompt }]},
            config={"configurable": {"thread_id": request.thread_id}},
        ) 
        """
        answer = result["messages"][-1].content
        print("the answer is : ", answer)
        if not answer:
            return {"answer": "Sorry I couldn't generate a repsonse please try again"}
        return {"answer": answer}
        """
        return StreamingResponse(
            get_chat_stream(
                message=request.prompt,
                thread_id=request.thread_id,
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            },
        )

            
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-pdf")
async def upload_def(file: UploadFile, thread_id: str = Form()):
    if not file:
        raise HTTPException(status_code=404, detail="no file uploaded")
    
    file_name = file.filename
    if not file_name or not file_name.endswith('.pdf'):
        raise HTTPException(status_code=401, detail="the file must be pdf")
    
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)
        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        agent.agents[thread_id] = agent.create_my_agent(file_path)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    finally:
        await file.close()
