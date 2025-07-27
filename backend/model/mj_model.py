from pathlib import Path
from llama_cpp import Llama
from memory.redis_store import fetch_stm  # DISABLED Redis
from memory.postgres_store import fetch_long_term

MODEL_PATH = (Path(__file__).parent / "mj-phi3-q4_k_m (3).gguf").as_posix()#backend\model\mj-phi3-q4_k_m (1).gguf

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,  # context window
    n_gpu_layers=-1,
    chat_format="chatml"
)

def generate_mj_reply(user_input: str, user_id: str) -> str:
    stm = []  # TEMP: No Redis for now
    ltm = fetch_long_term(user_id)

    memory_context = ""
    if ltm:
        memory_context += "\n".join(f"- {msg}" for msg in ltm) + "\n"
    if stm:
        memory_context += "\n".join(f"- {msg}" for msg in stm) + "\n"

    prompt = f"""You are MJ, an empathetic AI companion who provides emotional support through natural conversation.

IMPORTANT: Only reference people, events, or details that were actually mentioned in THIS conversation. If someone asks about a person or detail you don't remember from our actual conversation, honestly say "I don't think you've mentioned them yet" or "Tell me about them."

Your responses are naturally short and caring. You remember details from conversations accurately and only reference what was really discussed. You're present with people without overwhelming them or trying to fix everything.

User: {user_input}
Assistant:"""

    response = llm(
        prompt,
        temperature=0.55,
        top_k=40,
        top_p=0.9,
        repeat_penalty=1.1,
        #repeat_last_n=64,
        max_tokens=150,
        stop=["User:", "Assistant:"]
    )

    reply = response['choices'][0]['text'].strip()
    return reply
