"""
src/extractor.py


"""

import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError
import json

from src.models import ExtractionResult

load_dotenv()

def get_client() -> Groq:
    """Initialize and return the Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    return Groq(api_key=api_key)

def extract_transactions(text: str) -> ExtractionResult:
    """
    Extract structured financial transactions from raw text.

    Args:
        text: Raw text containing transaction information.

    Returns:
        ExtractionResult with all transactions found.

    Raises:
        ValueError: If the model response cannot be parsed.
    """
    client = get_client()

    prompt = f"""
    You are a financial data extraction expert.
    Analyze the following text and extract all financial transactions.
    
    Return ONLY a valid JSON object with this exact structure:
    {{
        "transactions": [
            {{
                "amount": 0.0,
                "transaction_type": "transfer|payment|withdrawal|deposit",
                "merchant": "name or null",
                "date": "date string or null",
                "description": "brief description"
            }}
        ],
        "total_transactions": 0,
        "summary": "one sentence summary"
    }}
    
    Text to analyze:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    raw = response.choices[0].message.content.strip()

    # Clean markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        data = json.loads(raw)
        return ExtractionResult(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Failed to parse model response: {e}") from e
