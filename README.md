# TicketFinder

TicketFinder is a Python app for scanning ticket listings across Ticketmaster, StubHub, and SeatGeek to surface potential ticket arbitrage opportunities in the United States.

It now includes:
- a CLI for terminal workflows
- a web interface for browser-based scans

## Features

- Pulls listings from three marketplaces through a common adapter interface.
- Supports US-wide scans or optional single-state filtering.
- Calculates projected profit and ROI with configurable buy/sell fee assumptions.
- Provides CLI output and a web UI.
- Includes tests for scanner behavior and web routes.

## Quickstart (local)
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
```

### Run CLI

```bash
ticketfinder "Taylor Swift" --state NY
```

### Run Web UI

```bash
uvicorn ticketfinder.web:app --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000`.

## Deploying the web app (inexpensive)

### Option A: Render (recommended cheapest/easiest managed path)
1. Push this repo to GitHub.
2. Create a new **Web Service** on Render.
3. Set:
   - **Build command**: `pip install -e .`
   - **Start command**: `uvicorn ticketfinder.web:app --host 0.0.0.0 --port $PORT`
4. Add environment variable `SEATGEEK_CLIENT_ID` (optional, for live SeatGeek data).
5. Deploy.

### Option B: Fly.io
- Use a Python app config and run the same start command above.

### Option C: VPS (lowest raw cost, more ops)
- Install Python + virtualenv.
- `pip install -e .`
- Run with systemd + reverse proxy (nginx/caddy).

## Live API notes

- `SeatGeekClient` supports live API calls when `SEATGEEK_CLIENT_ID` is set.
- `TicketmasterClient` and `StubHubClient` currently use fallback sample listings (replace with authenticated integrations in `platforms.py`).
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
- Real arbitrage is sensitive to latency, fees, taxes, payout delays, and listing quality.
- Add robust event identity resolution before production use (IDs differ by platform).
- Real arbitrage is sensitive to latency, fees, tax, payout delays, and listing quality.
- Add robust identity resolution before production use (event IDs differ by platform).
