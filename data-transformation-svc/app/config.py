from dotenv import load_dotenv
import os
load_dotenv()

# API and Model Configuration
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
DATA_CRUD_SERVICE_URL= os.getenv("DATA_CRUD_SERVICE_URL")
GROQ_API_KEY= os.getenv("GROQ_API_KEY")