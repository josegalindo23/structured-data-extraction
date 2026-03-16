# El primer código real del proyecto. 
# Extractor de datos estructurados de transacciones financieras
#  usando Claude + Pydantic. Simple, limpio, tipado — señal de producción desde el día 1.

"""
main.py

"""
import sys
from src.extractor import extract_transactions
from src.models import TransactionType

from src.utils import (
    load_text_file, filter_comments, summarize_by_currency, summarize_by_type,
    calculate_net_flow, export_to_json
)

ICONS = {
    TransactionType.TRANSFER: "↔",
    TransactionType.PAYMENT: "💳",
    TransactionType.WITHDRAWAL: "↑",
    TransactionType.DEPOSIT: "↓",
}

DEFAULT_FILE = "data/sample_transactions.txt"

def print_transactions(result):
    """Print transactions in a readable format."""
    for t in result.transactions:
        icon = ICONS.get(t.transaction_type, "•")
        print(
            f"  {icon} [{t.transaction_type.value.upper():10}] "
            f"{t.currency.value:7} {t.amount:>12,.0f}  —  {t.description}"
        )
        if t.merchant:
            print(f"     {'Merchant':10}: {t.merchant}")
        if t.date:
            print(f"     {'Date':10}: {t.date}")

def print_summary(result):
    """Print financial summary."""
    print("\n  — By Currency —")
    for currency, total in summarize_by_currency(result).items():
        print(f"     {currency:7}: {total:>14,.0f}")

    print("\n  — By Type —")
    for ttype, total in summarize_by_type(result).items():
        print(f"     {ttype:12}: {total:>14,.0f}")

    net = calculate_net_flow(result)
    print("\n  — Net Flow (same currency only) —")
    print(f"     Inflow  : {net['inflow']:>14,.0f}")
    print(f"     Outflow : {net['outflow']:>14,.0f}")
    print(f"     Net     : {net['net']:>14,.0f}")

    print(f"\n  Summary: {result.summary}")

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

    print(f"\n  Loading transactions from: {filepath}")
    raw_text = load_text_file(filepath)
    clean_text = filter_comments(raw_text)

    print("  Extracting transactions...\n")
    result = extract_transactions(clean_text)

    print(f"  Found {result.total_transactions} transactions\n")
    print_transactions(result)
    print_summary(result)

    export_to_json(result, "data/output.json")
    print("\n  Done.\n")

if __name__ == "__main__":
    main()