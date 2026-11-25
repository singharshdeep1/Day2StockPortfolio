
import csv
from pathlib import Path

from portfolio_data import PORTFOLIOS
from trade_checker import evaluate_trade


# Find the CSV file in the same folder
BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "trades_test.csv"
OUTPUT_FILE = BASE_DIR / "trade_results.csv"


def main():

    results = []

    # Read the input CSV
    with open(INPUT_FILE, mode="r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for trade in reader:

            portfolio_id = trade["portfolio_id"]

            # Find the relevant portfolio
            portfolio = PORTFOLIOS.get(portfolio_id)

            if portfolio is None:
                result = {
                    "decision": "Rejected",
                    "reason": "Portfolio reference data not found."
                }
            else:
                # Evaluate the proposed trade
                result = evaluate_trade(trade, portfolio)

            # Combine trade information and decision
            results.append({
                **trade,
                **result
            })

    # Write decisions to output CSV
    fieldnames = [
        "portfolio_id",
        "security_id",
        "action",
        "quantity",
        "price",
        "security_type",
        "decision",
        "reason"
    ]

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    # Display results
    print("\nPORTFOLIO TRADE COMPLIANCE RESULTS")
    print("=" * 55)

    for result in results:

        print(
            f"{result['portfolio_id']} | "
            f"{result['security_id']} | "
            f"{result['action']} | "
            f"{result['decision']}"
        )

        print(f"Reason: {result['reason']}")
        print("-" * 55)

    print(f"\nTotal trades processed: {len(results)}")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
