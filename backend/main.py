from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

from model.mj_model import generate_mj_reply
from memory.classifier import classify_memory_type
from memory.redis_store import store_in_redis
from memory.postgres_store import store_long_term

app = FastAPI()

# Allow frontend access from React/Vite (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ChatInput(BaseModel):
    user_id: str
    message: str

# Chat endpoint
@app.post("/chat")
async def chat(input: ChatInput):
    print(f"📨 Message from {input.user_id}: {input.message}")

    try:
        # Step 1: Classify memory type
        memory_type = classify_memory_type(input.message)
        print(f"🧠 Memory Type: {memory_type}")

        # Step 2: Store in correct memory
        if memory_type == "short-term memory":
            store_in_redis(input.user_id, input.message)

        elif memory_type == "long-term memory":
            store_long_term(input.user_id, input.message)

        elif memory_type == "short-term memory and long-term memory":
            store_in_redis(input.user_id, input.message)
            store_long_term(input.user_id, input.message)

        # Step 3: Generate reply from MJ
        reply = generate_mj_reply(input.message, input.user_id)
        return {
            "response": reply,
            "memory_type": memory_type
        }

    except Exception as e:
        print("❌ Error during chat:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="MJ failed to process the message.")