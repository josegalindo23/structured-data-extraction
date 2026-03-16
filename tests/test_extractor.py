"""
test/test_extractor.py


"""

from src.models import ExtractionResult, Transaction, TransactionType, Currency


def test_extraction_result_structure():
    """ExtractionResult must contain valid transactions."""
    transaction = Transaction(
        amount=450000.0,
        transaction_type=TransactionType.TRANSFER,
        currency=Currency.COP,
        merchant="Maria",
        date="yesterday",
        description="rent payment",
    )
    result = ExtractionResult(
        transactions=[transaction],
        total_transactions=1,
        summary="One rent transfer to Maria.",
    )
    assert result.total_transactions == 1
    assert result.transactions[0].amount == 450000.0
    assert result.transactions[0].transaction_type == TransactionType.TRANSFER
    assert result.transactions[0].currency == Currency.COP


def test_transaction_optional_fields():
    """Merchant and date must be optional."""
    transaction = Transaction(
        amount=50000.0,
        transaction_type=TransactionType.PAYMENT,
        currency=Currency.USD,
        description="anonymous payment",
    )
    assert transaction.merchant is None
    assert transaction.date is None

def test_transaction_type_enum_values():
    """TransactionType enum must have exactly the four valid values."""
    valid_types = {t.value for t in TransactionType}
    assert valid_types == {"transfer", "payment", "withdrawal", "deposit"}


def test_currency_enum_values():
    """Currency enum must include the main world currencies."""
    currencies = {c.value for c in Currency}
    assert "COP" in currencies
    assert "USD" in currencies
    assert "EUR" in currencies
    assert "UNKNOWN" in currencies

def test_multi_currency_result():
    """ExtractionResult must handle transactions in different currencies."""
    transactions = [
        Transaction(
            transaction_type=TransactionType.DEPOSIT,
            amount=1800000.0,
            currency=Currency.COP,
            description="salary deposit",
        ),
        Transaction(
            transaction_type=TransactionType.PAYMENT,
            amount=32.0,
            currency=Currency.USD,
            description="lunch delivery",
            merchant="Rappi",
        ),
    ]
    result = ExtractionResult(
        transactions=transactions,
        total_transactions=2,
        summary="Two transactions in different currencies.",
    )
    currencies_in_result = {t.currency for t in result.transactions}
    assert Currency.COP in currencies_in_result
    assert Currency.USD in currencies_in_result