from typing import AsyncGenerator
from agent import current_agent
import asyncio

async def get_chat_stream(message: str, thread_id: str) -> AsyncGenerator[str, None]:
    
    if not current_agent:
        yield "data: ERROR: Upload PDF first\n\n"
        return
    try:
        async for chunk, metadata in current_agent.astream(
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            },
            stream_mode="messages",
        ):

            if chunk and chunk.content:
                yield f"data: {chunk.content}\n\n"
                await asyncio.sleep(0.1)
    except Exception as e:
        yield f"data: ERROR: {str(e)}\n\n"