from __future__ import annotations

import argparse
from dataclasses import asdict
from json import dumps

from .scanner import ArbitrageScanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ticketfinder",
        description="Scan US ticket marketplaces for ticket arbitrage opportunities.",
    )
    parser.add_argument("event", help="Event search term (e.g. 'Taylor Swift').")
    parser.add_argument("--state", help="Optional 2-letter state filter (e.g. NY).")
    parser.add_argument("--min-profit", type=float, default=15.0, help="Minimum projected profit in USD.")
    parser.add_argument("--min-roi", type=float, default=0.08, help="Minimum projected ROI as decimal.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    scanner = ArbitrageScanner(min_profit=args.min_profit, min_roi=args.min_roi)
    opportunities = scanner.scan(event_query=args.event, state=args.state)

    if args.json:
        payload = [asdict(item) for item in opportunities]
        print(dumps(payload, indent=2))
        return

    if not opportunities:
        print("No profitable opportunities found for current filters.")
        return

    print(f"Found {len(opportunities)} opportunity(s):")
    for idx, item in enumerate(opportunities, start=1):
        print(
            f"{idx}. {item.event_name} [{item.city}, {item.state}] "
            f"{item.section}-{item.row} x{item.quantity} | "
            f"Buy {item.buy_platform} @ ${item.buy_price:.2f}, "
            f"Sell {item.sell_platform} @ ${item.sell_price:.2f}, "
            f"Profit ${item.estimated_profit:.2f}, ROI {item.roi:.2%}"
        )


if __name__ == "__main__":
    main()
