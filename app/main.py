from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from app.database import init_mock_db, execute_read_query
from app.security import sanitize_and_validate_sql
from app.engine import generate_sql_from_text

load_dotenv()
init_mock_db()

app = FastAPI(title="Enterprise Semantic Search API")

class SearchRequest(BaseModel):
    prompt: str

@app.post("/search")
async def execute_semantic_search(request: SearchRequest):
    generated_sql = generate_sql_from_text(request.prompt)
    validated_sql = sanitize_and_validate_sql(generated_sql)
    results = execute_read_query(validated_sql)
    
    return {
        "status": "success",
        "executed_query": validated_sql,
        "count": len(results),
        "data": results
    }