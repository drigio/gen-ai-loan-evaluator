from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import applicant, transaction, key_financial_indicator
from app.db import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow only these origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

async def startup_event():
    init_db()

app.add_event_handler("startup", startup_event)

app.include_router(applicant.router)
app.include_router(transaction.router)
app.include_router(key_financial_indicator.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)