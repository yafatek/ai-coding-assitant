import logging
import time
import uuid

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from agents.CodingAgent import CodingAgent
from loggers.Logger import Logger

logger = Logger()
# In-memory data store for chats
chats = {}

app = FastAPI()


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    chat_id = str(uuid.uuid4())  # Create a new chat ID for this connection
    chats[chat_id] = {
        "id": chat_id,
        "title": "WebSocket Chat",
        "messages": [],
        "createdAt": time.time(),
        "updatedAt": time.time()
    }
    try:
        while True:
            data = await websocket.receive_text()

            # Add user message to chat history
            user_message = {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": data,
                "timestamp": time.time()
            }
            chats[chat_id]["messages"].append(user_message)

            # Generate AI response using Gemini
            agent = CodingAgent(chat_id='chat_id', api_key="GEMINI_API_KEY")
            code = await agent.generate_code(data)
            ai_message = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": code,
                "timestamp": time.time()
            }
            chats[chat_id]["messages"].append(ai_message)
            chats[chat_id]["updatedAt"] = time.time()

            await websocket.send_json(ai_message)  # Send the AI message back

    except WebSocketDisconnect:
        logging.info(f"WebSocket connection closed for chat ID: {chat_id}")


if __name__ == "__main__":
    # Run the server with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=11203)
