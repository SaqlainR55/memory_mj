from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from memory.redis_store import fetch_stm
from memory.postgres_store import fetch_long_term

MERGED_MODEL_PATH = (Path(__file__).parent / "phi3_merged_mj").as_posix()

tokenizer = AutoTokenizer.from_pretrained(
    MERGED_MODEL_PATH,
    trust_remote_code=False
)

model = AutoModelForCausalLM.from_pretrained(
    MERGED_MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=False
)

if getattr(model.config, "sliding_window", None) is not None:
    model.config.sliding_window = None

if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id


def generate_mj_reply(user_input: str, user_id: str) -> str:
    # 1. Fetch memories
    stm = fetch_stm(user_id)
    ltm = fetch_long_term(user_id)

    # 2. Create memory context for internal use (not shown to user)
    memory_context = ""
    if ltm:
        memory_context += "\n".join(f"- {msg}" for msg in ltm) + "\n"
    if stm:
        memory_context += "\n".join(f"- {msg}" for msg in stm) + "\n"

    # 3. Construct the internal prompt (for model only)
    prompt = f"""You are MJ, a helpful and friendly AI assistant who remembers conversations.
{memory_context if memory_context else ''}
Respond naturally and helpfully to the user.

User: {user_input}
Assistant:"""

    # 4. Tokenize and prepare input
    input_ids = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
    ).to(model.device)

    # 5. Generate MJ's reply
    output = model.generate(
        input_ids=input_ids["input_ids"],
        attention_mask=input_ids["attention_mask"],
        max_new_tokens=200,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    # 6. Decode and return **only the assistant's reply**
    decoded = tokenizer.decode(output[0], skip_special_tokens=True)

    # Extract reply after last "Assistant:"
    if "Assistant:" in decoded:
        return decoded.split("Assistant:")[-1].strip()
    else:
        return decoded.strip()
