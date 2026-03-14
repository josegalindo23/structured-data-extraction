# El primer código real del proyecto. 
# Extractor de datos estructurados de transacciones financieras
#  usando Claude + Pydantic. Simple, limpio, tipado — señal de producción desde el día 1.

"""
main.py

"""

from src.extractor import extract_transactions


SAMPLE_TEXT = """
    Yesterday I transferred 450,000 pesos to Maria for rent.
    Also paid 32,000 pesos at Rappi for lunch delivery.
    Withdrew 200,000 pesos from Bancolombia ATM on Friday.
    Received a deposit of 1,800,000 pesos from my employer on the 1st.
"""


def main():
    print("Extracting transactions...\n")
    result = extract_transactions(SAMPLE_TEXT)

    for t in result.transactions:
        print(f"  [{t.transaction_type.upper()}] ${t.amount:,.0f} — {t.description}")
        if t.merchant:
            print(f"    Merchant: {t.merchant}")
        if t.date:
            print(f"    Date: {t.date}")

    print(f"\nTotal: {result.total_transactions} transactions")
    print(f"Summary: {result.summary}")


if __name__ == "__main__":
    main()