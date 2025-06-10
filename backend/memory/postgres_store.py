import psycopg2

def store_long_term(user_id: str, message: str):
    try:
        conn = psycopg2.connect(
            dbname="mj_memory_test",
            user="postgres",
            password="mj123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id SERIAL PRIMARY KEY,
                user_id TEXT,
                message TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute(
            "INSERT INTO long_term_memory (user_id, message) VALUES (%s, %s);",
            (user_id, message)
        )

        conn.commit()
        print(f"✅ Stored in PostgreSQL: {message}")

    except Exception as e:
        print(f"❌ PostgreSQL Error: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def fetch_long_term(user_id: str):
    """Fetch all long-term memory entries for a user."""
    try:
        conn = psycopg2.connect(
            dbname="mj_memory_test",
            user="postgres",
            password="mj123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT message FROM long_term_memory
            WHERE user_id = %s
            ORDER BY timestamp ASC;
        """, (user_id,))

        rows = cur.fetchall()
        messages = [row[0] for row in rows]
        print(f"📥 Retrieved LTM for {user_id}: {messages}")
        return messages

    except Exception as e:
        print(f"❌ Error fetching PostgreSQL data: {e}")
        return []

    finally:
        if conn:
            cur.close()
            conn.close()