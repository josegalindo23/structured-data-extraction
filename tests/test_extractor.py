"""
test/test_extractor.py


"""

from src.models import ExtractionResult, Transaction


def test_extraction_result_structure():
    """ExtractionResult must contain valid transactions."""
    transaction = Transaction(
        amount=450000.0,
        transaction_type="transfer",
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
    assert result.transactions[0].transaction_type == "transfer"


def test_transaction_optional_fields():
    """Merchant and date must be optional."""
    transaction = Transaction(
        amount=50000.0,
        transaction_type="payment",
        description="anonymous payment",
    )
    assert transaction.merchant is None
    assert transaction.date is None