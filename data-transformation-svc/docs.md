# Technical Documentation: Data Transformation Service

## Project Overview

The `data-transformation-svc` is a RESTful service designed to process bank statements. It extracts data from bank statement PDFs, stores the raw text, and uses an LLM (Language Learning Model) to extract transaction details in CSV format. This data is then stored using a separate service (`data-crud-svc`).

**Key Functionality:**

1.  **PDF Parsing:** Parses bank statement PDFs using `pdfplumber` to extract the raw text.
2.  **Data Storage (Raw Text):** Stores the extracted raw text in a database by updating the Applicant's information via the `data-crud-svc`.
3.  **Transaction Extraction:** Sends the raw text to an OpenAI-compatible LLM (specifically mentioning Groq) with a prompt to extract transactions in CSV format.
4.  **Data Storage (Transactions):** Stores the extracted transaction data in the database, associating it with the respective applicant using the `data-crud-svc`.
5. **Data Models:** Uses Pydantic models for data validation and structuring (Applicant, Transaction, KeyFinancialIndicator).
6. **Asynchronous Operations:** Uses `asyncio` and `aiohttp` for asynchronous operations for better performance, especially for I/O-bound tasks like network requests.

**Technology Stack:**

*   **Programming Language:** Python
*   **Framework:** FastAPI
*   **PDF Parsing:** pdfplumber
*   **LLM Interaction:** OpenAI API (Groq)
*   **Asynchronous HTTP Client:** aiohttp
*   **Environment Variables:** python-dotenv
* **Data Models/Validation**: Pydantic

## API Endpoints

The service exposes the following RESTful API endpoint:

### `POST /api/v1/process-bank-statement`

**Description:** Processes an uploaded bank statement PDF, extracts the raw text, and then extracts transaction data using an LLM. Stores both the raw text and extracted transactions using the `data-crud-svc`.

**Request:**

*   **Method:** `POST`
*   **Content-Type:** `multipart/form-data`
*   **Body:**
    *   `file`: (File) The bank statement PDF file.

**Response:**

*   **Status Codes:**
    *   `200 OK`: Bank statement processed successfully.
    *   `400 Bad Request`: Invalid file format (not a PDF).
    *   `404 Not Found`: Applicant not found (during update).
    *   `422 Unprocessable Entity`: Validation error
    *   `500 Internal Server Error`: Any other error during processing.
*   **Body (Success):**
    ```json
    {
        "message": "Bank statement processed and transactions extracted successfully",
        "applicant_id": "string"
    }
    ```

## Internal Components and Logic

### 1. `main.py`

*   **Entry Point:** Initializes the FastAPI application.
*   **Event Handlers:** Includes a `startup` event handler that initializes the `DataCRUDClient`.  This client is stored in the application's state (`app.state.data_crud_client`) for later use by route handlers, ensuring a single instance is shared across requests.
*   **Route Inclusion:** Includes the `process_bank_statement` router.

### 2. `config.py`

*   **Configuration Management:** Loads environment variables using `python-dotenv`.
*   **Configuration Values:**
    *   `GROQ_BASE_URL`: Base URL for the Groq API.
    *   `LLM_MODEL`: The specific LLM model to use.
    *   `DATA_CRUD_SERVICE_URL`: The base URL for the `data-crud-svc`.
    *   `GROQ_API_KEY`: API Key for authenticating with Groq service

### 3. `routes/process_bank_statement.py`

*   **Endpoint Definition:** Defines the `/process-bank-statement` endpoint.
*   **File Handling:** Accepts a PDF file upload using FastAPI's `UploadFile`.
*   **Content Type Validation:** Checks if the uploaded file is a PDF.  Raises a 400 error if not.
*   **Workflow:**
    1.  **Parse PDF:** Calls `parse_pdf` (from `app.services.pdf_parser`) to extract text from the PDF.
    2.  **Create Applicant:** Calls `create_applicant` to create a new applicant in `data-crud-svc` and retrieves applicant id.
    3.  **Update Applicant with Raw Text:**  Calls `update_applicant_with_raw_text` to store the extracted raw text with the applicant.
    4.  **Process and Store Transactions:** Calls `process_and_store_transactions` to extract transaction data via the LLM and store it.
*   **Error Handling:** Uses `try...except` blocks to handle potential `HTTPException` and other exceptions, returning appropriate HTTP status codes and error details.
* **Helper Functions:**
    * `create_applicant`: Creates new applicant using data-crud-svc
    * `update_applicant_with_raw_text`: Updates the created applicant using data-crud-svc with raw bank statement text
    * `process_and_store_transactions`: Sends the raw text to LLM and extracts the transaction information as a list of dictionaries.
    *   `convert_datetime_to_string`: Converts date time object to string before sending data to data-crud-svc, because date time object is not json serializable

### 4. `services/pdf_parser.py`

*   **`parse_pdf(file_path)`:**
    *   Takes either a file path (string) or file bytes as input.
    *   Uses `pdfplumber.open()` to open the PDF.
    *   Calls the internal `_extract_text` function to get the text.
    *   Handles potential exceptions during PDF processing.
*   **`_extract_text(pdf)`:**
    *   Iterates through each page of the PDF.
    *   Extracts text from each page using `page.extract_text()`.
    *   Joins the text from all pages into a single string.

### 5. `services/llm_processor.py`

*   **`process_text_with_llm(statement_text)`:**
    *   Constructs the messages for the LLM, including the `TRANSACTION_EXTRACTION_PROMPT` and the extracted bank statement text.
    *   Uses the `openai.AsyncOpenAI` client (configured with Groq's base URL and API key) to send a chat completion request to the LLM.  This is done *asynchronously*.
    *   Extracts the generated CSV content from the LLM's response.
    *   Cleans up the generated CSV data using regular expressions to ensure it conforms to the specified format and to remove any extraneous text added by the model.
    *   Calls `_parse_csv_to_transactions` to parse the CSV data.
*   **`_parse_csv_to_transactions(csv_content)`:**
    *   Uses Python's built-in `csv.DictReader` to parse the CSV string into a list of dictionaries.  Each dictionary represents a transaction.
    *   Handles potential errors during CSV parsing.

### 6. `services/data_crud_client.py`

*   **`DataCRUDClient`:** A class to encapsulate interactions with the `data-crud-svc`.
*   **Methods:** Provides methods to interact with the `data-crud-svc` API:
    *   `create_applicant(applicant_data)`: Creates a new applicant.
    *   `update_applicant(applicant_id, applicant_data)`: Updates an existing applicant.
    *   `create_transactions(applicant_id, transactions)`: Creates multiple transactions for an applicant.
    *   `create_kfi(applicant_id, kfi_data)`: Creates Key Financial Indicators for an applicant.
    *   `get_applicant(applicant_id)`: Retrieves a specific applicant by ID.
*   **Asynchronous Requests:** Uses `aiohttp.ClientSession()` to make asynchronous HTTP requests to the `data-crud-svc`.

### 7. `utils/prompts.py`

*   **`TRANSACTION_EXTRACTION_PROMPT`:**  Defines the prompt used to instruct the LLM on how to extract transaction data from the bank statement text.  This prompt is crucial for accurate data extraction.  It clearly specifies:
    *   The role of the LLM ("You are given...")
    *   The input data format (unstructured bank statement text).
    *   The desired output format (CSV).
    *   The specific fields to extract (Date, Description, Transaction\_Type, Amount, Balance, Currency).
    *   Detailed instructions for formatting, including date format, handling of double quotes in descriptions, and ensuring amount is positive.
    *   A clear instruction to output *only* the CSV data.

### 8. `models/`

*   Defines Pydantic models for data validation and structuring. This ensures type safety and data consistency.
    *   **`applicant.py`:** Defines the `Applicant` model.
    *   **`transaction.py`:** Defines the `Transaction` model.
    *   **`key_financial_indicator.py`:** Defines the `KeyFinancialIndicator` model.

## Data-CRUD-SVC API Endpoints

The `data-transformation-svc` relies on the following API endpoints provided by the `data-crud-svc`. These are documented in the provided `project_desc.md` file.

### Applicant Endpoints

*   `POST /applicants/`
*   `GET /applicants/`
*   `GET /applicants/{applicant_id}`
*   `PUT /applicants/{applicant_id}`
*   `DELETE /applicants/{applicant_id}`

### Transaction Endpoints

*   `POST /applicants/{applicant_id}/transactions/`
* `POST /applicants/{applicant_id}/transactions/bulk/`
*   `GET /applicants/{applicant_id}/transactions/`
*   `GET /applicants/{applicant_id}/transactions/{transaction_id}`
*   `PUT /applicants/{applicant_id}/transactions/{transaction_id}`
*   `DELETE /applicants/{applicant_id}/transactions/{transaction_id}`

### Key Financial Indicator (KFI) Endpoints

*   `POST /applicants/{applicant_id}/kfi/`
*   `GET /applicants/{applicant_id}/kfi/{kfi_id}`
*   `PUT /applicants/{applicant_id}/kfi/{kfi_id}`

## Error Handling

*   **HTTP Exceptions:** The code uses `fastapi.HTTPException` to raise errors that should be returned as HTTP responses. This includes handling invalid file types (400), applicant not found (404), and internal server errors (500).
*   **Data Validation Errors:** The `DataCRUDClient` handles potential 422 errors (Unprocessable Entity) from the `data-crud-svc`, which would indicate validation errors.  These are logged.
*   **General Exceptions:** `try...except` blocks are used to catch general exceptions during PDF parsing, LLM processing, and interactions with the `data-crud-svc`.

## Summary

The `data-transformation-svc` is a well-structured FastAPI service that efficiently processes bank statements.  It leverages asynchronous programming, external services (Groq and `data-crud-svc`), and clear prompts to extract structured data from unstructured PDF documents. The use of Pydantic models, a separate data access client, and comprehensive error handling contributes to the service's robustness and maintainability. The service successfully converts unstructured data from bank statements into structured transaction data.