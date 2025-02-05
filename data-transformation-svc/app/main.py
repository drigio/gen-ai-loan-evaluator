from fastapi import FastAPI
from app.routes import process_bank_statement
from app.services.data_crud_client import DataCRUDClient

app = FastAPI(title="Data Ingestion Service", version="1.0.0")


async def startup_event():
    app.state.data_crud_client = DataCRUDClient()

app.add_event_handler("startup", startup_event)

app.include_router(process_bank_statement.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)