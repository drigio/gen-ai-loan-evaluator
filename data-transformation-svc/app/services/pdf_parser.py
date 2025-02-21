import pdfplumber
import io
from typing import Optional, Union
import inspect

def parse_pdf(file_path: Union[str, bytes]) -> Optional[str]:
    print("Reached " + inspect.currentframe().f_code.co_name)
    try:
        if isinstance(file_path, str):
            with pdfplumber.open(file_path) as pdf:
                return _extract_text(pdf)
        elif isinstance(file_path, bytes):
            with pdfplumber.open(io.BytesIO(file_path)) as pdf:
                return _extract_text(pdf)
        else:
            raise ValueError("Invalid input type. Expected string path or bytes.")
    except Exception as e:
        print(f"Error parsing PDF: {str(e)}")
        return None

def _extract_text(pdf) -> str:
    print("Reached " + inspect.currentframe().f_code.co_name)
    full_text = []
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    return "\n".join(full_text).strip()