"""
src/utils.py

"""
from pathlib import Path
from src.models import ExtractionResult, TransactionType


def load_text_file(filepath: str) -> str:
    """
    Load text content from a file.

    Args:
        filepath: Path to the text file.

    Returns:
        File content as string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return path.read_text(encoding="utf-8")


def filter_comments(text: str) -> str:
    """
    Remove comment lines (starting with #) from text.

    Args:
        text: Raw text possibly containing comment lines.

    Returns:
        Clean text without comment lines.
    """
    lines = [
        line for line in text.splitlines()
        if not line.strip().startswith("#") and line.strip()
    ]
    return "\n".join(lines)


def summarize_by_currency(result: ExtractionResult) -> dict[str, float]:
    """
    Group and sum transaction amounts by currency.

    Args:
        result: ExtractionResult containing transactions.

    Returns:
        Dictionary mapping currency code to total amount.
    """
    totals: dict[str, float] = {}
    for t in result.transactions:
        key = t.currency.value
        totals[key] = totals.get(key, 0.0) + t.amount
    return totals


def summarize_by_type(result: ExtractionResult) -> dict[str, float]:
    """
    Group and sum transaction amounts by transaction type.

    Args:
        result: ExtractionResult containing transactions.

    Returns:
        Dictionary mapping transaction type to total amount.
    """
    totals: dict[str, float] = {}
    for t in result.transactions:
        key = t.transaction_type.value
        totals[key] = totals.get(key, 0.0) + t.amount
    return totals


def calculate_net_flow(result: ExtractionResult) -> dict[str, float]:
    """
    Calculate inflow, outflow and net balance from transactions.
    Note: amounts in different currencies are not comparable —
    this is only meaningful for single-currency result sets.

    Args:
        result: ExtractionResult containing transactions.

    Returns:
        Dictionary with inflow, outflow and net keys.
    """
    inflow_types = {TransactionType.DEPOSIT}
    outflow_types = {
        TransactionType.PAYMENT,
        TransactionType.WITHDRAWAL,
        TransactionType.TRANSFER,
    }
    inflow = sum(
        t.amount for t in result.transactions
        if t.transaction_type in inflow_types
    )
    outflow = sum(
        t.amount for t in result.transactions
        if t.transaction_type in outflow_types
    )
    return {
        "inflow": inflow,
        "outflow": outflow,
        "net": inflow - outflow,
    }


def export_to_json(result: ExtractionResult, filepath: str) -> None:
    """
    Export extraction result to a JSON file.

    Args:
        result: ExtractionResult to export.
        filepath: Destination file path.
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    print(f"  Exported to {filepath}")