# API Endpoints Documentation

This document describes the RESTful endpoints available in the application.

## Applicant Endpoints

Defined in `applicant.py`.

### Create Applicant
* **Method:** POST
* **Path:** `/applicants/`
* **Description:** Creates a new applicant.
* **Request Body:** `Applicant` model (defined in `applicant.py`).
* **Response Body:** `Applicant` model with generated `id`.

### Get Applicants
* **Method:** GET
* **Path:** `/applicants/`
* **Description:** Retrieves a list of all applicants (excluding soft-deleted).
* **Response Body:** List of `Applicant` models.

### Get Applicant by ID
* **Method:** GET
* **Path:** `/applicants/{applicant_id}`
* **Description:** Retrieves a specific applicant by ID (excluding soft-deleted).
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to retrieve.
* **Response Body:** `Applicant` model.
* **Error Response:** 404 Not Found if applicant is not found.

### Update Applicant by ID
* **Method:** PUT
* **Path:** `/applicants/{applicant_id}`
* **Description:** Updates an existing applicant by ID.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to update.
* **Request Body:** `Applicant` model (defined in `applicant.py`).
* **Response Body:** Updated `Applicant` model.
* **Error Response:** 404 Not Found if applicant is not found.

## Transaction Endpoints

Defined in `transaction.py`.

### Create Transaction
* **Method:** POST
* **Path:** `/applicants/{applicant_id}/transactions/`
* **Description:** Creates a new transaction for a specific applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to associate the transaction with.
* **Request Body:** `Transaction` model (defined in `transaction.py`).
* **Response Body:** `Transaction` model with generated `id`.

### Get Transactions for Applicant
* **Method:** GET
* **Path:** `/applicants/{applicant_id}/transactions/`
* **Description:** Retrieves a list of transactions for a specific applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant to retrieve transactions for.
* **Response Body:** List of `Transaction` models (or potentially a list of transaction dictionaries based on `get_transactions` return type, further clarification needed in `transaction.py` routes file).

### Get Transaction by ID
* **Method:** GET
* **Path:** `/applicants/{applicant_id}/transactions/{transaction_id}`
* **Description:** Retrieves a specific transaction by ID for a given applicant (excluding soft-deleted).
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `transaction_id`: ID of the transaction to retrieve.
* **Response Body:** `Transaction` model.
* **Error Response:** 404 Not Found if transaction is not found.

### Update Transaction by ID
* **Method:** PUT
* **Path:** `/applicants/{applicant_id}/transactions/{transaction_id}`
* **Description:** Updates an existing transaction by ID for a given applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `transaction_id`: ID of the transaction to update.
* **Request Body:** `Transaction` model (defined in `transaction.py`).
* **Response Body:** Updated `Transaction` model.
* **Error Response:** 404 Not Found if transaction is not found.

### Delete Transaction by ID (Soft Delete)
* **Method:** DELETE
* **Path:** `/applicants/{applicant_id}/transactions/{transaction_id}`
* **Description:** Soft deletes a transaction by ID for a given applicant. Marks `is_deleted` as true.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `transaction_id`: ID of the transaction to delete.
* **Response Body:** `{ "message": "Transaction soft deleted" }`.
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
* **Response Body:** `KeyFinancialIndicator` model with generated `id`.

### Get KFI by ID
* **Method:** GET
* **Path:** `/applicants/{applicant_id}/kfi/{kfi_id}`
* **Description:** Retrieves a specific KFI by ID for a given applicant (excluding soft-deleted).
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `kfi_id`: ID of the KFI to retrieve.
* **Response Body:** `KeyFinancialIndicator` model.
* **Error Response:** 404 Not Found if KFI is not found.

### Update KFI by ID
* **Method:** PUT
* **Path:** `/applicants/{applicant_id}/kfi/{kfi_id}`
* **Description:** Updates an existing KFI by ID for a given applicant.
* **Path Parameters:**
    * `applicant_id`: ID of the applicant.
    * `kfi_id`: ID of the KFI to update.
* **Request Body:** `KeyFinancialIndicator` model (defined in `key_financial_indicator.py`).
* **Response Body:** Updated `KeyFinancialIndicator` model.
* **Error Response:** 404 Not Found if KFI is not found.

**Note:** This documentation assumes standard RESTful endpoint conventions based on the code structure. For complete and accurate documentation, you should refer to the route definitions in `applicant.py`, `transaction.py`, and `key_financial_indicator.py` files, specifically looking for `@router.post`, `@router.get`, `@router.put`, and `@router.delete` decorators and their associated paths. You may also want to check for any route parameters defined using FastAPI's path parameter syntax (e.g., `{item_id}`).