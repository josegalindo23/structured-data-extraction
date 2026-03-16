""""
mod
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    """Valid transaction types for financial operations."""
    TRANSFER = "transfer"
    PAYMENT = "payment"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"

class Currency(str, Enum):
    """Most used currencies worldwide."""
    COP = "COP"
    USD = "USD"
    EUR = "EUR"
    MXN = "MXN"
    BRL = "BRL"
    ARS = "ARS"
    GBP = "GBP"
    JPY = "JPY"
    UNKNOWN = "UNKNOWN"

class Transaction(BaseModel):
    "Represents a financial transaction extracted from text."
    amount: float = Field(description="Transaction amount in Colomnian pesos.")
    transaction_type: TransactionType = Field(description="Type of the transaction.")
    currency: Currency = Field(default=Currency.UNKNOWN, description="Currency of the transaction.")
    merchant: Optional[str] = Field(default=None, description="Merchant of recipient name.")
    date: Optional[str] = Field(default=None, description="Date mentioned in the text.")
    description: str = Field(description="Brief description of the transaction.")

class ExtractionResult(BaseModel):
    """Result of extracting transactions from text input."""
    transactions: list[Transaction] 
    total_transactions: int
    summary: str


