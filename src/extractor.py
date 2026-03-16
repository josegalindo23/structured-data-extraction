"""
src/extractor.py


"""

import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError
import json
from google import genai
from anthropic import Anthropic
from openai import OpenAI

from src.models import ExtractionResult

load_dotenv()

PROMPT_TEMPLATE = """
    You are a financial data extraction expert.
    Analyze the following text and extract all financial transactions.
    The text may be in any language — always respond in English.
    
    Return ONLY a valid JSON object with this exact structure, no markdown, no explanation:
    {{
        "transactions": [
            {{
                "amount": 0.0,
                "transaction_type": "transfer|payment|withdrawal|deposit",
                "currency": "COP|USD|EUR|MXN|BRL|ARS|GBP|JPY|UNKNOWN",
                "merchant": "name or null",
                "date": "date string or null",
                "description": "brief description"
            }}
        ],
        
        "total_transactions": 0,
        "summary": "one sentence summary in English"
    }}

    Rules:
    - amount must be a plain number, no symbols, no commas (450000 not $450,000)
    - transaction_type must be exactly one of: transfer, payment, withdrawal, deposit
    - currency must be detected from context (symbols, words, country references)
    - merchant and date are null if not mentioned
    - always respond in English regardless of input language
    
    Text to analyze:
    {text}
    """

def _parse_response(raw: str) -> ExtractionResult:
    """"Parse and validate the raw JSON response from any LLM provider."""

    # Clean markdown code blocks if present
    raw = raw.strip()
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

def _extract_with_gemini(text: str) -> ExtractionResult:
    """Extract transactions using Google Gemini 2.0 Flash."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")
    client = genai.Client(api_key = api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=PROMPT_TEMPLATE.format(text=text),
    )
    return _parse_response(response.text)

def _extract_with_anthropic(text: str) -> ExtractionResult:
    """Extract transactions using Anthropic Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found.")
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(text=text)}],
    )
    return _parse_response(response.choices[0].text)

def _extract_with_openrouter(text: str) -> ExtractionResult:
    """Extract transactions OpenRouter."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found.")
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(text=text)}],
        temperature=0.1,
    )
    return _parse_response(response.choices[0].message.content)

def _extract_with_groq(text: str) -> ExtractionResult:
    """Extract transactions using Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(text=text)}],
        temperature=0.1,
    )
    return _parse_response(response.choices[0].message.content)

# Provider registry — order defines priority
# PROVIDERS = [
#     ("gemini", _extract_with_gemini),
#     ("groq", _extract_with_groq),
#     ("anthropic", _extract_with_anthropic),
#     ("openrouter", _extract_with_openrouter),
# ]

PROVIDERS = [
    ("anthropic", _extract_with_anthropic),
    ("openrouter", _extract_with_openrouter),
    ("gemini", _extract_with_gemini),
    ("groq", _extract_with_groq),
]

def extract_transactions(text: str) -> ExtractionResult:
    """
    Extract structured financial transactions from raw text.
    Automatically falls back to the next provider if one fails.
    Supports any input language — always returns English output.

    Args:
        text: Raw text containing transaction information in any language.

    Returns:
        ExtractionResult with all transactions found.

    Raises:
        RuntimeError: If all providers fail.
    """
    errors: list[str] = []

    for provider_name, provider_fn in PROVIDERS:
        try:
            print(f"  Trying provider: {provider_name}...")
            result = provider_fn(text)
            print(f"  Success with: {provider_name}\n")
            return result
        except Exception as e:
            print(f"  {provider_name} failed: {type(e).__name__}")
            errors.append(f"{provider_name}: {e}")

    raise RuntimeError("All providers failed:\n" + "\n".join(errors))