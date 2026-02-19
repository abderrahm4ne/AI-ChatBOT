import json
from typing import AsyncGenerator
from ..agent import current_agent

async def get_chat_stream(message: str, thread_id: str) -> AsyncGenerator[str, None]:
    """
    Asynchronous generator.
    """
    
    async for chunk, metadata in current_agent.astream(  
    input= {"messages": [{"role": "user", "content": message}]},
    stream_mode="messages",
    ):
        if chunk.content:
            yield chunk.content

    yield "data: [DONE]\n\n"