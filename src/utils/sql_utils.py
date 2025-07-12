# utils/sql_utils.py
import re


# clears query 
def clean_sql(sql):
    
    # Remove code block markers and triple quotes (```sql, ```, """sql, etc.)
    sql = re.sub(r'^[`"]{3,}.*$', '', sql, flags=re.MULTILINE)
    sql = sql.replace('```', '').replace('"""', '')
    # Remove leading/trailing whitespace
    return sql.strip()


#blocks deleting data 
def is_read_only(sql: str) -> bool:
    sql = sql.strip().lower()
    return sql.startswith("select") and not any(
        keyword in sql for keyword in ["insert", "update", "delete", "drop", "alter", "truncate", "create"]
    )