# El primer código real del proyecto. 
# Extractor de datos estructurados de transacciones financieras
#  usando Claude + Pydantic. Simple, limpio, tipado — señal de producción desde el día 1.

"""
main.py

"""

from src.extractor import extract_transactions
from src.models import TransactionType

ICONS = {
    TransactionType.TRANSFER: "↔",
    TransactionType.PAYMENT: "💳",
    TransactionType.WITHDRAWAL: "↑",
    TransactionType.DEPOSIT: "↓",
}

# SAMPLE_TEXT = """
#     Yesterday I transferred 450,000 pesos to Maria for rent.
#     Also paid 32,000 pesos at Rappi for lunch delivery.
#     Withdrew 200,000 pesos from Bancolombia ATM on Friday.
#     Received a deposit of 1,800,000 pesos from my employer on the 1st.
# """

# Multi-language, multi-currency test
SAMPLE_TEXT = """
    Yesterday I transferred 450,000 pesos colombianos to Maria for rent.
    Also paid $32 dollars at Rappi for lunch delivery.
    Retiré 200 euros en el cajero del Santander el viernes.
    Received a deposit of 1,800,000 COP from my employer on the 1st.
"""

def print_result(result):
    for t in result.transactions:
        icon = ICONS.get(t.transaction_type, "•")
        print(f"  {icon} [{t.transaction_type.value.upper()}] "
              f"{t.currency.value} {t.amount:,.0f} — {t.description}")
        if t.merchant:
            print(f"     Merchant : {t.merchant}")
        if t.date:
            print(f"     Date     : {t.date}")

    by_currency = {}
    for t in result.transactions:
        by_currency.setdefault(t.currency.value, []).append(t.amount)

    print("\n  Totals by currency:")
    for currency, amounts in by_currency.items():
        print(f"     {currency}: {sum(amounts):,.0f}")

    print(f"\n  Summary: {result.summary}")
    print("\n--- Raw JSON ---")
    print(result.model_dump_json(indent=2))


def main():
    print("Extracting transactions...\n")
    result = extract_transactions(SAMPLE_TEXT)
    print_result(result)


if __name__ == "__main__":
    main()