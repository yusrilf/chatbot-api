import asyncio
import uvicorn
from typing import AsyncIterable

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from pydantic import BaseModel
from train import chain

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    content: str



chat_history = []
async def generate_answer(question):
    global chat_history
    query = "Prompt: Kamu adalah chatbot tanya jawab cerdas untuk menjawab pertanyaan seputar komponen cadangan. menjawab menggunakan bahasa indonesia dengan jelas dan lengkap. jawablah sesuai data yang saya berikan diembedding "+question

    # Create an asyncio.Future to store the response
    response_future = asyncio.Future()

    # Generate the response character by character
    async for char in chain.astream({"question": query, "chat_history": chat_history}):
        chat_history.append((query, char['answer']))
        response_future.set_result(char['answer'])

    # Return the completed response
    return await response_future
    
    

async def send_message(content: str) :

    results = await asyncio.gather(generate_answer(content))
    
    try:
        if results and results[0]:
            for char in results[0]:
                # Yield each character with a delay to simulate typing
                yield char
                await asyncio.sleep(0.01) # Mengakses 'answer' dari hasil pertama
    except Exception as e:
        print(f"Caught exception: {e}")


@app.post("/stream_chat/")
async def stream_chat(message: Message):
    generator = send_message(message.content)
    return StreamingResponse(generator, media_type="text/event-stream")