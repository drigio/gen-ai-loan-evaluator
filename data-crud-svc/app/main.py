from fastapi import FastAPI
from app.routes import applicant, transaction, key_financial_indicator
from app.db import init_db

app = FastAPI()

async def startup_event():
    init_db()

app.add_event_handler("startup", startup_event)

app.include_router(applicant.router)
app.include_router(transaction.router)
app.include_router(key_financial_indicator.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)