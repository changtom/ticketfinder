# TicketFinder

TicketFinder is a Python CLI app that scans ticket listings across Ticketmaster, StubHub, and SeatGeek to surface potential ticket arbitrage opportunities in the United States.

## Features

- Pulls listings from three major marketplaces through a common adapter interface.
- Supports US-wide scans or single-state filtering.
- Calculates projected profit and ROI with configurable buy/sell fee assumptions.
- Outputs either human-readable text or JSON for automation.
- Includes tests for scanner behavior and filters.

## How it works

1. Fetch listings from each platform client.
2. Normalize each listing into a shared schema.
3. Group listings by event + seating location.
4. Compare cross-platform buy/sell directions.
5. Keep only opportunities above configured `min_profit` and `min_roi`.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
ticketfinder "Taylor Swift" --state NY
```

JSON output:

```bash
ticketfinder "NBA Finals" --json
```

## Live API notes

- `SeatGeekClient` supports live API calls when `SEATGEEK_CLIENT_ID` is set.
- `TicketmasterClient` and `StubHubClient` currently use fallback sample listings (you can replace with authenticated API integrations in `platforms.py`).

## Example output

```text
Found 2 opportunity(s):
1. Taylor Swift Live [Los Angeles, CA] 202-F x2 | Buy ticketmaster @ $95.00, Sell stubhub @ $150.00, Profit $59.80, ROI 27.87%
2. Taylor Swift Tour [Chicago, IL] 310-C x4 | Buy seatgeek @ $72.00, Sell ticketmaster @ $120.00, Profit $92.16, ROI 28.56%
```

## Important considerations

- Respect each platform's Terms of Service and robots policies.
- Real arbitrage is sensitive to latency, fees, tax, payout delays, and listing quality.
- Add robust identity resolution before production use (event IDs differ by platform).
