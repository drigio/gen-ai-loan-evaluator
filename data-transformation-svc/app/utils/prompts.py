TRANSACTION_EXTRACTION_PROMPT = (
    """
You are given an unstructured bank statement text from any region, in any currency (e.g., INR, USD, GBP), and with variable formatting. Your task is to extract the transaction data and present it in CSV format. For each transaction, extract:

- **Date**: The date of the transaction (formatted as YYYY-MM-DD).
- **Description**: The transaction description or payee. Keep it inside double quotes (""). If there are already double quotes in the description text, handle this by escaping it by doubling the quotes within the field. For example, if a cell contains a value like He said ""Hello, world!"", it would be written as ""He said """
    "Hello, world!"
    """""
- **Transaction_Type**: "credit" if money is coming into the account(credit), or "debit" if money is going out(debit).
- **Amount**: The transaction amount as a positive number.
- **Balance**: The account balance after the transaction (if available).
- **Currency**: The currency used in the transaction (e.g., INR, USD, GBP).

Format the extracted data as CSV with the following headers:

```
date,description,transaction_type,amount,balance,currency
```

Only output the CSV data with one transaction per line and no additional text or explanations.
    """
)
