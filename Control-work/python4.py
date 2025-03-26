from fastapi import FastAPI
from factorial_service import app as factorial_app
from deduplication_service import app as deduplication_app
from linked_list_service import app as linked_list_app

app = FastAPI(title="Algorithm Services", version="1.0.0")

app.mount("/factorials", factorial_app)
app.mount("/deduplicate", deduplication_app)
app.mount("/linked-list", linked_list_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
