# memory/redis_store.py

import redis

# Redis client
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def store_in_redis(user_id, message):
    key = f"user:{user_id}:stm"
    r.rpush(key, message)
    print(f"✅ Stored in Redis: {message}")

def fetch_stm(user_id):
    """Fetch all short-term memory messages for the user."""
    key = f"user:{user_id}:stm"
    messages = r.lrange(key, 0, -1)
    print(f"📥 Retrieved STM for {user_id}: {messages}")
    return messages