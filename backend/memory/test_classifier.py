import sys
import os

# Allow importing from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memory.classifier import classify_memory_type
from memory.redis_store import store_in_redis
from memory.postgres_store import store_long_term

# Sample prompts (simulate user interaction)
samples = [
    "remind me tomorrow to take my pills",
    "my birthday is January 5th",
    "assume I like Indian food whenever booking restaurants",
    "save this as both long and short term memory"
]

# Simulated user
user_id = "user123"

# Classify and store each prompt
for prompt in samples:
    memory_type = classify_memory_type(prompt)
    print(f"🧠 Prompt: {prompt}\n🧾 Predicted Memory Type: {memory_type}\n")

    if memory_type == "short-term memory":
        store_in_redis(user_id, prompt)

    elif memory_type == "long-term memory":
        store_long_term(user_id, prompt)

    elif memory_type == "short-term memory and long-term memory":
        store_in_redis(user_id, prompt)
        store_long_term(user_id, prompt)