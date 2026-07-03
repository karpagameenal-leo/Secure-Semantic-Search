import sqlite3

# Initialize an in-memory or local file database
DB_FILE = "company_data.db"

def init_mock_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create a mock products/inventory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            security_rating TEXT NOT NULL
        )
    """)
    
    # Insert mock entries if table is empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ("ProtonMail Plus", "Software", 4.99, 9999, "A+"),
            ("ProtonVPN Visionary", "Software", 9.99, 500, "A+"),
            ("Encrypted Storage Drive", "Hardware", 89.99, 120, "A"),
            ("Hardware Security Key", "Hardware", 45.00, 350, "A+"),
            ("Standard Router", "Hardware", 59.99, 10, "B")
        ]
        cursor.executemany("INSERT INTO products (name, category, price, stock, security_rating) VALUES (?, ?, ?, ?, ?)", mock_data)
        conn.commit()
    
    conn.close()

# Run database setup on startup
init_mock_db()

import re
from fastapi import HTTPException

def sanitize_and_validate_sql(raw_sql: str) -> str:
    """
    Cleans the LLM output and enforces strict read-only execution guardrails.
    """
    # 1. Strip markdown formatting block code indicators standard to LLM responses
    cleaned_sql = raw_sql.replace("```sql", "").replace("```", "").strip()
    
    # 2. Convert to uppercase for unified regex checking
    upper_sql = cleaned_sql.upper()
    
    # 3. Enforce Strict Read-Only Policy (No modifications allowed)
    forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "GRANT", "REPLACE"]
    for word in forbidden_keywords:
        if re.search(r'\b' + word + r'\b', upper_sql):
            raise HTTPException(
                status_code=400, 
                detail=f"Security Violation: Generated query contains forbidden structural keyword: '{word}'."
            )
            
    # 4. Enforce that the query MUST start with a SELECT operation
    if not upper_sql.startswith("SELECT"):
        raise HTTPException(
            status_code=400, 
            detail="Security Violation: The system rejected a non-SELECT statement structural query."
        )
        
    return cleaned_sql

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

# Initialize the Groq Client. 
# Make sure to set your environment variable: set GROQ_API_KEY="your_api_key"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a highly secure, deterministic text-to-SQL translation engine.
Your sole job is to convert natural language requests into valid SQLite queries based strictly on the schema provided below.

Table Name: products
Schema:
- id (INTEGER)
- name (TEXT)
- category (TEXT)
- price (REAL)
- stock (INTEGER)
- security_rating (TEXT)

CRITICAL RULES:
1. Return ONLY the raw SQL query string. Do NOT wrap it in commentary, explanations, or code blocks.
2. Only generate SELECT statements. Do not attempt modification operations under any circumstance.
3. If a query cannot be answered by this schema, reply with: SELECT * FROM products WHERE 1=0;
4. Use the LOWER() function for all string comparisons (e.g., LOWER(category) = 'software').
"""

def generate_sql_from_text(user_query: str) -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate this request to SQL: {user_query}"}
            ],
            model="openai/gpt-oss-120b", # Fast, high-intelligence model tracking minimal footprints
            temperature=0.0,         # Force deterministic, predictable output
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Processing Error: {str(e)}")

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="Secure Semantic Search Engine")

class SearchRequest(BaseModel):
    prompt: str

@app.post("/search")
async def execute_semantic_search(request: SearchRequest):
    # Step A: Translate the text request to raw SQL string
    generated_sql = generate_sql_from_text(request.prompt)
    
    # Step B: Pass it through our verification firewall
    validated_sql = sanitize_and_validate_sql(generated_sql)
    
    # Step C: Secure execution phase
    try:
        conn = sqlite3.connect(DB_FILE)
        # Configure row factory to return list of dictionaries instead of raw tuples
        conn.row_factory = lambda cursor, row: dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
        cursor = conn.cursor()
        
        cursor.execute(validated_sql)
        results = cursor.fetchall()
        conn.close()
        
        return {
            "status": "success",
            "executed_query": validated_sql,
            "count": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Execution Error: {str(e)}")