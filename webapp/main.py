# main.py
from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
# import aiofiles
from typing import Dict

app = FastAPI()

# Mount static files and templates because we are using Jinja2. Jinja2 is a templating engine for Python.
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Replace with your OpenAI API key
# openai.api_key = "your_openai_api_key_here"

# CORS middleware is required to allow requests from the frontend
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add a global variable to store conversation history
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

# Add a constant for maximum memory tokens
MAX_MEMORY_TOKENS = 70

# root function to render index.html
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# chat function to handle chat requests
@app.post("/api/chat")
async def chat_endpoint(request: Request, body: Dict[str, str] = Body(...)):
    user_message = body.get("user_message")
    if not user_message:
        raise HTTPException(status_code=400, detail="user_message is required")

    conversation_history.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model="gpt-4", # OR gpt-3.5-turbo
        messages=conversation_history,
    )

    assistant_message = response.choices[0].message["content"]
    conversation_history.append({"role": "assistant", "content": assistant_message})

    # Remove older messages when total tokens in conversation_history exceed MAX_MEMORY_TOKENS
    while response.usage['total_tokens'] > MAX_MEMORY_TOKENS:
        # Ensure that there are at least two messages (one "system" and one other message) before removing a message
        if len(conversation_history) > 2:
            removed_message = conversation_history.pop(1)  # Skip the "system" message at index 0
            # Create a new API call without the removed_message
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation_history,
            )
        else:
            break

    return assistant_message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
