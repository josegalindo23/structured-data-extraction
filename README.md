<div align="center">

# 💸 Structured Data Extraction

**Extract structured / messy financial transactions from any text — any language, any format, any currency.**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![Tests](https://img.shields.io/badge/Tests-5%20passed-22C55E?style=flat&logo=pytest&logoColor=white)](./tests)
[![Code style](https://img.shields.io/badge/Code%20style-Ruff-FFA500?style=flat)](https://docs.astral.sh/ruff)

</div>

---

## What does it do?

Takes Structured, messy, unstructured text — WhatsApp messages, bank SMS, emails, statements — and returns clean, validated financial data ready to use in any system.

**Input** (any format, any language):
```
[10:23] Juan: listo te mande los 80mil del almuerzo
Bancolombia: Su cuenta fue debitada por $45.990 en NETFLIX
You received $320.000 from Carlos Mejia - freelance payment
```

**Output** (structured, typed, validated):
```json
{
  "transactions": [
    { "transaction_type": "transfer", "amount": 80000, "currency": "COP", "description": "lunch payment" },
    { "transaction_type": "withdrawal", "amount": 45990, "currency": "COP", "merchant": "NETFLIX" },
    { "transaction_type": "deposit", "amount": 320000, "currency": "COP", "merchant": "Carlos Mejia" }
  ],
  "total_transactions": 3,
  "summary": "Three transactions totaling 445,990 COP."
}
```

---

## Key Features

| Feature | Details |
|---|---|
| 🌍 Any language | Spanish, English, Portuguese — detect and extract regardless |
| 💱 Multi-currency | COP, USD, EUR, MXN, BRL, ARS, GBP, JPY auto-detected |
| 🔄 Provider fallback | Gemini → Groq → Anthropic → OpenRouter — never a single point of failure |
| ✅ Fully validated | Pydantic V2 with enums — invalid data raises clear errors |
| 📁 Any input format | WhatsApp, SMS, emails, plain text, bank statements |

---

## Architecture
```
Input text (any format)
        │
        ▼
┌───────────────────┐
│   filter_comments │  ← removes metadata and noise
└────────┬──────────┘
         │
         ▼
┌───────────────────────────────────────┐
│         Provider Fallback Chain       │
│                                       │
│  1. Gemini 2.0 Flash                  │
│  2. Groq  (Llama 3.3 70B)   ← active  │
│  3. Anthropic Claude Haiku            │
│  4. OpenRouter (Nemotron)             │
└────────┬──────────────────────────────┘
         │
         ▼
┌───────────────────┐
│  Pydantic V2      │  ← validates and types the response
│  ExtractionResult │
└────────┬──────────┘
         │
         ▼
  Typed Python objects
  + JSON export
```

---

## 🏗️ Resilience in Action (The Fallback Pattern)
This project is built for production. If one AI provider is down or hits a rate limit, the system automatically tries the next one in the chain:

```
Trying provider: gemini...
  ⚠️ gemini failed: 429 RESOURCE_EXHAUSTED (Rate limit)
Trying provider: groq...
  ✅ Success with: groq (Llama 3.3 70B)
```

---

## Tech Stack

- **[Python 3.13](https://python.org)** — core language
- **[Pydantic V2](https://docs.pydantic.dev)** — data validation and typing
- **[Groq](https://groq.com)** — primary LLM provider (Llama 3.3 70B)
- **[Google Gemini](https://ai.google.dev)** — secondary provider
- **[Anthropic Claude](https://anthropic.com)** — tertiary provider
- **[OpenRouter](https://openrouter.ai)** — quaternary provider
- **[pytest](https://pytest.org)** — test suite
- **[Ruff](https://docs.astral.sh/ruff)** — linter and formatter

---

## Quick Start
```bash
# 1. Clone
git clone https://github.com/josegalindo23/structured-data-extraction
cd structured-data-extraction

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your keys

# 5. Run with default sample
python main.py

# 6. Run with your own file
python main.py path/to/your/transactions.txt
```

---

## Environment Variables

Create a `.env` file based on `.env.example`:
```env
GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
ANTHROPIC_API_KEY=your-anthropic-key
OPENROUTER_API_KEY=your-openrouter-key
```

The system uses whichever keys are available — you don't need all four.

---

## Running Tests
```bash
pytest tests/ -v
```
```
tests/test_extractor.py::test_extraction_result_structure    PASSED
tests/test_extractor.py::test_transaction_optional_fields    PASSED
tests/test_extractor.py::test_transaction_type_enum_values   PASSED
tests/test_extractor.py::test_currency_enum_values           PASSED
tests/test_extractor.py::test_multi_currency_result          PASSED

```

---

## Project Structure
```
structured-data-extraction/
├── src/
│   ├── models.py          # Pydantic models — Transaction, ExtractionResult, enums
│   ├── extractor.py       # LLM providers + fallback chain
│   └── utils.py           # File loading, summaries, JSON export
├── tests/
│   └── test_extractor.py  # Unit tests
├── data/
│   ├── sample_transactions.txt   # Structured sample input
│   └── messy_input.txt           # Unstructured real-world sample
├── .env.example
├── requirements.txt
└── main.py
```

---

## Known Limitations

| Issue | Example | Status |
|---|---|---|
| Decimal vs thousand separator ambiguity | `$89.99` → `8999.0` in some locales | Known — out of scope |
| Future/hypothetical transactions included | `"Can you lend me $100?"` → extracted as transfer | Known — prompt improvement needed |
| Missing amount transactions ignored | `"Payroll transfer (no amount)"` → correctly skipped | Expected behavior |
| Ambiguous currency defaults to UNKNOWN | `"850 biweekly"` → `UNKNOWN` currency | Expected behavior |

---

## License

MIT — free to use, modify and distribute.

---

<div align="center">
  <sub>Built as part of an AI Engineer portfolio — focused on production-ready patterns.</sub>
</div>