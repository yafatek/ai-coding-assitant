# WebSocket Chat with Coding Agent

This project is a WebSocket-based chat application using **FastAPI** to provide real-time chat functionality. It integrates with a custom **CodingAgent** class to interact with the **Gemini API** for generating code responses based on user input. The project includes robust chat history storage and retrieval using **Redis** as an in-memory data store. It also includes safety filters for content moderation and custom tools for enhanced interactions.

## Features

- **WebSocket Chat Interface**: Enables real-time bi-directional communication with users.
- **Code Generation with Gemini API**: Uses the Gemini API to generate code responses based on user prompts.
- **Chat History Storage**: Stores chat messages and responses in Redis for session persistence.
- **Safety Filters**: Implements customizable safety settings for handling potentially harmful content.
- **Custom Tool Integrations**: Adds functionality with `search_custom_engine` and `scrape_website` tools.

## Project Structure

- **main.py**: Contains the main application code with the WebSocket endpoint and FastAPI setup.
- **CodingAgent Class**:
  - Manages interactions with the Gemini API.
  - Retrieves chat history from Redis and stores interactions.
  - Configures safety settings for content moderation.
- **Logger**: A custom logger that logs important application events and information, enhancing debugging and traceability.
- **RedisMemory**: Manages conversation history storage using Redis for efficient access.

## How It Works

1. **WebSocket Connection**: When a client connects to `/chat`, a WebSocket connection is established, and a new chat session is created with a unique `chat_id`.
2. **User Message Handling**: When a message is received, it’s stored in Redis and passed to the `CodingAgent`.
3. **AI Response Generation**: The `CodingAgent` sends the user message to the Gemini API to generate a response, which is then sent back to the user.
4. **Memory Management**: The chat history is maintained in Redis for the current session and loaded when required.

## Dependencies

- **FastAPI**: For building the WebSocket server and managing routes.
- **Uvicorn**: ASGI server to run FastAPI applications.
- **Google Generative AI**: For generating AI responses (Gemini API).
- **Redis**: Used for storing chat history and session management.

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/yafatek/ai-coding-assitant.git
```
```bash
 cd websocket-coding-agent
```
Install the required dependencies:
### Docker:
you need a Docker Desktop to run a Redis Instance
```bash
docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
```bash
pip install -r requirements.txt
```
Configure environment variables, including the Gemini API key and Redis connection details.

Run the application:

```bash 
uvicorn main:app --host 0.0.0.0 --port 11203
```
## Usage
Start the server.
Connect to the WebSocket endpoint at /chat.
Send a text message, and the application will respond with AI-generated code from the Gemini API.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
MIT License

Copyright (c) 2024 YAFATEK Solutions

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
