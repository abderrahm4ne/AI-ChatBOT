from typing import AsyncGenerator
import agent
import asyncio

async def get_chat_stream(message: str, thread_id: str) -> AsyncGenerator[str, None]:
    
    if not agent.current_agent:
        yield "data: ERROR: Upload PDF first\n\n"
        return
    try:
        async for chunk in agent.current_agent.astream(
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            },
            config={"configurable": {"thread_id": thread_id}},
            stream_mode="messages",
        ):
            if chunk:
                content = chunk.content
                if isinstance(content, list):
                    for item in content: # gemini output
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text = item.get('text', '')
                            if text:
                                yield f"data: {text}\n\n"
                elif isinstance(content, str) and content: # for groq
                    yield f"data: {content}\n\n"
                
                await asyncio.sleep(0.05)
    except Exception as e:
        yield f"data: ERROR: {str(e)}\n\n"