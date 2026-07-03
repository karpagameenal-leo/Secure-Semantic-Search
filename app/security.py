import re
from fastapi import HTTPException

def sanitize_and_validate_sql(raw_sql: str) -> str:
    cleaned_sql = raw_sql.replace("```sql", "").replace("```", "").strip()
    upper_sql = cleaned_sql.upper()
    
    forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "GRANT", "REPLACE"]
    for word in forbidden_keywords:
        if re.search(r'\b' + word + r'\b', upper_sql):
            raise HTTPException(status_code=400, detail=f"Security Violation: Forbidden keyword '{word}' detected.")
            
    if not upper_sql.startswith("SELECT"):
        raise HTTPException(status_code=400, detail="Security Violation: Non-SELECT queries are blocked.")
        
    return cleaned_sql