import os
from groq import Groq
from fastapi import HTTPException

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a secure, deterministic text-to-SQL engine.
Convert natural language to an SQLite query using this schema:
Table: products (id, name, category, price, stock, security_rating)
Rules: 
1. Output RAW SQL string only. No markdown wrappers.
2. Only SELECT statements allowed.
3. Use LOWER() for string filters (e.g. LOWER(category) = 'software').
"""

def generate_sql_from_text(user_query: str, model_name: str = "openai/gpt-oss-120b") -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate: {user_query}"}
            ],
            model=model_name,
            temperature=0.0,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")