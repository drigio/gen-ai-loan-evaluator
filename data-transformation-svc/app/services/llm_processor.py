import os
from typing import List, Dict
import csv
from openai import AsyncOpenAI
from dotenv import load_dotenv
from app.config import GROQ_BASE_URL, LLM_MODEL, GROQ_API_KEY
from app.utils.prompts import TRANSACTION_EXTRACTION_PROMPT
import inspect
import re


load_dotenv()

client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


async def process_text_with_llm(statement_text: str) -> List[Dict[str, str]]:
    print("Reached " + inspect.currentframe().f_code.co_name)
    messages = [
        {"role": "system", "content": TRANSACTION_EXTRACTION_PROMPT},
        {"role": "user", "content": statement_text},
    ]

    try:
        response = await client.chat.completions.create(
            model=LLM_MODEL, messages=messages, temperature=0.3, max_tokens=12000
        )
        generated_csv = response.choices[0].message.content.strip()
        cleaned_csv = re.sub(r"<think>.*?</think>", "", generated_csv, flags=re.DOTALL)
        cleaned_csv = re.sub(r"^```csv\s*", "", cleaned_csv, flags=re.DOTALL)
        cleaned_csv = cleaned_csv.replace("```", "").strip()

        return _parse_csv_to_transactions(cleaned_csv)
    except Exception as e:
        print(f"Error processing text with LLM: {str(e)}")
        return []


def _parse_csv_to_transactions(csv_content: str) -> List[Dict[str, str]]:
    print("Reached " + inspect.currentframe().f_code.co_name)
    transactions = []
    # print(csv_content)
    # print("CSV CONTENT ENDS HERE ===============================")
    try:
        csv_reader = csv.DictReader(line.strip() for line in csv_content.splitlines())
        for row in csv_reader:
            transactions.append(row)
    except Exception as e:
        print(f"Error parsing CSV content: {e}")
        return []
    # print(transactions)
    return transactions
