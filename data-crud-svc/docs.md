# API Endpoints Documentation

This document describes the RESTful endpoints available in the application.

## Applicant Endpoints

Defined in `applicant.py`.

### Create Applicant
* **Method:** POST
* **Path:** `/applicants/`
* **Description:** Creates a new applicant.
* **Request Body:** `Applicant` model (defined in `applicant.py`).
    ```json
    {
        "name": "John Doe",
        "bank_statement_pdf_path": "/path/to/pdf",
        "raw_bank_statement_txt": "text content"
    }
    ```
* **Response Body:** `Applicant` model with generated `id`.
    ```json
    {
        "id": "6543b53a16954536a8cb1711",
        "name": "John Doe",
        "bank_statement_pdf_path": "/path/to/pdf",
        "raw_bank_statement_txt": "text content",
        "transactions": [],
        "key_financial_indicators": null
    }
    ```

### Get Applicants
* **Method:** GET
* **Path:** `/applicants/`
* **Description:** Retrieves a list of all applicants (excluding soft-deleted).
* **Response Body:** List of `Applicant` models.
    ```json
    [
        {
            "id": "6543b53a16954536a8cb1711",
            "name": "John Doe",
            "bank_statement_pdf_path": "/path/to/pdf",
            "raw_bank_statement_txt": "text content",
            "transactions": [],
            "key_financial_indicators": null
        },
        {
            "id": "6543b53a16954536a8cb1712",
            "name": "Jane Doe",
            "bank_statement_pdf_path": "/path/to/another/pdf",
            "raw_bank_statement_txt": "another text content",
            "transactions": [],
            "key_financial_indicators": null
        }
    
    ```

### Get Applicant by ID
* **Method:** GET
* **Path:** `/applicants/{applicant_id}`
* **Description:** Retrieves a specific applicant by ID (excluding soft-deleted).
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to retrieve.
* **Response Body:** `Applicant` model.
    ```json
    {
        "id": "6543b53a16954536a8cb1711",
        "name": "John Doe",
        "bank_statement_pdf_path": "/path/to/pdf",
        "raw_bank_statement_txt": "text content",
        "transactions": [],
        "key_financial_indicators": null
    }
    ```
* **Error Response:** 404 Not Found if applicant is not found.

### Update Applicant by ID
* **Method:** PUT
* **Path:** `/applicants/{applicant_id}`
* **Description:** Updates an existing applicant by ID.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to update.
* **Request Body:** `Applicant` model (defined in `applicant.py`).
    ```json
    {
        "name": "Updated John Doe",
        "bank_statement_pdf_path": "/path/to/updated/pdf",
        "raw_bank_statement_txt": "updated text content"
    }
    ```
* **Response Body:** Updated `Applicant` model.
    ```json
    {
        "id": "6543b53a16954536a8cb1711",
        "name": "Updated John Doe",
        "bank_statement_pdf_path": "/path/to/updated/pdf",
        "raw_bank_statement_txt": "updated text content",
        "transactions": [],
        "key_financial_indicators": null
    }
    ```
* **Error Response:** 404 Not Found if applicant is not found.

### Delete Applicant by ID (Soft Delete)
* **Method:** DELETE
* **Path:** `/applicants/{applicant_id}`
* **Description:** Soft deletes an applicant by ID. Marks `is_deleted` as true.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to delete.
* **Response Body:** `{ "message": "Applicant soft deleted" }`.
    ```json
    { "message": "Applicant soft deleted" }
    ```

## Transaction Endpoints

Defined in `transaction.py`.

### Create Transaction
* **Method:** POST
* **Path:** `/applicants/{applicant_id}/transactions/`
* **Description:** Creates a new transaction for a specific applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to associate the transaction with.
* **Request Body:** `Transaction` model (defined in `transaction.py`).
    ```json
    {
        "date": "2024-01-01",
        "description": "Grocery Store",
        "transaction_type": "debit",
        "amount": 50.00,
        "balance": 1000.00,
        "currency": "USD"
    }
    ```
* **Response Body:** `Transaction` model with generated `id`.
    ```json
    {
        "id": "6543b53a16954536a8cb1721",
        "date": "2024-01-01",
        "description": "Grocery Store",
        "transaction_type": "debit",
        "amount": 50.00,
        "balance": 1000.00,
        "currency": "USD"
    }
    ```

### Get Transactions for Applicant
* **Method:** GET
* **Path:** `/applicants/{applicant_id}/transactions/`
* **Description:** Retrieves a list of transactions for a specific applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to retrieve transactions for.
* **Response Body:** List of `Transaction` models.
    ```json
    [
        {
            "id": "6543b53a16954536a8cb1721",
            "date": "2024-01-01",
            "description": "Grocery Store",
            "transaction_type": "debit",
            "amount": 50.00,
            "balance": 1000.00,
            "currency": "USD"
        },
        {
            "id": "6543b53a16954536a8cb1722",
            "date": "2024-01-02",
            "description": "Online Shopping",
            "transaction_type": "debit",
            "amount": 100.00,
            "balance": 900.00,
            "currency": "USD"
        }
    ]
    ```

### Get Transaction by ID
* **Method:** GET
* **Path:** `/applicants/{applicant_id}/transactions/{transaction_id}`
* **Description:** Retrieves a specific transaction by ID for a given applicant (excluding soft-deleted).
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `transaction_id`: ID of the transaction to retrieve.
* **Response Body:** `Transaction` model.
    ```json
    {
        "id": "6543b53a16954536a8cb1721",
        "date": "2024-01-01",
        "description": "Grocery Store",
        "transaction_type": "debit",
        "amount": 50.00,
        "balance": 1000.00,
        "currency": "USD"
    }
    ```
* **Error Response:** 404 Not Found if transaction is not found.

### Update Transaction by ID
* **Method:** PUT
* **Path:** `/applicants/{applicant_id}/transactions/{transaction_id}`
* **Description:** Updates an existing transaction by ID for a given applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `transaction_id`: ID of the transaction to update.
* **Request Body:** `Transaction` model (defined in `transaction.py`).
    ```json
    {
        "date": "2024-01-01",
        "description": "Updated Grocery Store",
        "transaction_type": "debit",
        "amount": 55.00,
        "balance": 995.00,
        "currency": "USD"
    }
    ```
* **Response Body:** Updated `Transaction` model.
    ```json
    {
        "id": "6543b53a16954536a8cb1721",
        "date": "2024-01-01",
        "description": "Updated Grocery Store",
        "transaction_type": "debit",
        "amount": 55.00,
        "balance": 995.00,
        "currency": "USD"
    }
    ```
* **Error Response:** 404 Not Found if transaction is not found.

### Delete Transaction by ID (Soft Delete)
* **Method:** DELETE
* **Path:** `/applicants/{applicant_id}/transactions/{transaction_id}`
* **Description:** Soft deletes a transaction by ID for a given applicant. Marks `is_deleted` as true.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `transaction_id`: ID of the transaction to delete.
* **Response Body:** `{ "message": "Transaction soft deleted" }`.
    ```json
    { "message": "Transaction soft deleted" }
    ```
* **Error Response:** 404 Not Found if transaction is not found.


## Key Financial Indicator (KFI) Endpoints

Defined in `key_financial_indicator.py`.

### Create KFI
* **Method:** POST
* **Path:** `/applicants/{applicant_id}/kfi/`
* **Description:** Creates a new Key Financial Indicator (KFI) for a specific applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to associate the KFI with.
* **Request Body:** `KeyFinancialIndicator` model (defined in `key_financial_indicator.py`).
    ```json
    {
        "monthly_income": 3000.00,
        "monthly_expenses": 1500.00,
        "net_monthly_income": 1500.00,
        "income_coefficient_of_variation": 0.1,
        "expense_coefficient_of_variation": 0.2,
        "savings_rate": 0.5,
        "average_account_balance": 5000.00,
        "liquidity_ratio": 2.0,
        "number_of_overdrafts": 0,
        "income_stability_score": 0.8,
        "expense_stability_score": 0.7,
        "savings_rate_score": 0.9,
        "liquidity_ratio_score": 0.85,
        "overdraft_penalty_score": 1.0
    }
    ```
* **Response Body:** `KeyFinancialIndicator` model with generated `id`.
    ```json
    {
        "id": "6543b53a16954536a8cb1731",
        "monthly_income": 3000.00,
        "monthly_expenses": 1500.00,
        "net_monthly_income": 1500.00,
        "income_coefficient_of_variation": 0.1,
        "expense_coefficient_of_variation": 0.2,
        "savings_rate": 0.5,
        "average_account_balance": 5000.00,
        "liquidity_ratio": 2.0,
        "number_of_overdrafts": 0,
        "income_stability_score": 0.8,
        "expense_stability_score": 0.7,
        "savings_rate_score": 0.9,
        "liquidity_ratio_score": 0.85,
        "overdraft_penalty_score": 1.0
    }
    ```

### Get KFI by ID
* **Method:** GET
* **Path:** `/applicants/{applicant_id}/kfi/{kfi_id}`
* **Description:** Retrieves a specific KFI by ID for a given applicant (excluding soft-deleted).
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `kfi_id`: ID of the KFI to retrieve.
* **Response Body:** `KeyFinancialIndicator` model.
    ```json
    {
        "id": "6543b53a16954536a8cb1731",
        "monthly_income": 3000.00,
        "monthly_expenses": 1500.00,
        "net_monthly_income": 1500.00,
        "income_coefficient_of_variation": 0.1,
        "expense_coefficient_of_variation": 0.2,
        "savings_rate": 0.5,
        "average_account_balance": 5000.00,
        "liquidity_ratio": 2.0,
        "number_of_overdrafts": 0,
        "income_stability_score": 0.8,
        "expense_stability_score": 0.7,
        "savings_rate_score": 0.9,
        "liquidity_ratio_score": 0.85,
        "overdraft_penalty_score": 1.0
    }
    ```
* **Error Response:** 404 Not Found if KFI is not found.

### Update KFI by ID
* **Method:** PUT
* **Path:** `/applicants/{applicant_id}/kfi/{kfi_id}`
* **Description:** Updates an existing KFI by ID for a given applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `kfi_id`: ID of the KFI to update.
* **Request Body:** `KeyFinancialIndicator` model (defined in `key_financial_indicator.py`).
    ```json
    {
        "monthly_income": 3500.00,
        "monthly_expenses": 1600.00,
        "net_monthly_income": 1900.00,
        "income_coefficient_of_variation": 0.15,
        "expense_coefficient_of_variation": 0.25,
        "savings_rate": 0.55,
        "average_account_balance": 5500.00,
        "liquidity_ratio": 2.2,
        "number_of_overdrafts": 1,
        "income_stability_score": 0.85,
        "expense_stability_score": 0.75,
        "savings_rate_score": 0.95,
        "liquidity_ratio_score": 0.90,
        "overdraft_penalty_score": 0.9
    }
    ```
* **Response Body:** Updated `KeyFinancialIndicator` model.
    ```json
    {
        "id": "6543b53a16954536a8cb1731",
        "monthly_income": 3500.00,
        "monthly_expenses": 1600.00,
        "net_monthly_income": 1900.00,
        "income_coefficient_of_variation": 0.15,
        "expense_coefficient_of_variation": 0.25,
        "savings_rate": 0.55,
        "average_account_balance": 5500.00,
        "liquidity_ratio": 2.2,
        "number_of_overdrafts": 1,
        "income_stability_score": 0.85,
        "expense_stability_score": 0.75,
        "savings_rate_score": 0.95,
        "liquidity_ratio_score": 0.90,
        "overdraft_penalty_score": 0.9
    }
    ```