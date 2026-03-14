""""
mod
"""
from pydantic import BaseModel, Field
from typing import Optional


class Transaction(BaseModel):
    "Represents a financial transaction extracted from text."
    amount: float = Field(description="Transaction amount in Colomnian pesos.")
    transaction_type: str = Field(description="Type: transfer, payment, withdrawal, deposit.")
    merchant: Optional[str] = Field(default=None, description="Merchant of recipient name.")
    date: Optional[str] = Field(default=None, description="Date mentioned in the text.")
    description: str = Field(description="Brief description of the transaction.")

class ExtractionResult(BaseModel):
    """Result of extracting transactions from text input."""
    transactions: list[Transaction] 
    total_transactions: int
    summary: str


