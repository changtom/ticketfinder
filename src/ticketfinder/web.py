from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .scanner import ArbitrageScanner

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="TicketFinder", version="0.2.0")


@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    event: str | None = Query(default=None),
    state: str | None = Query(default=None, min_length=2, max_length=2),
    min_profit: float = Query(default=15.0, ge=0),
    min_roi: float = Query(default=0.08, ge=0),
) -> HTMLResponse:
    opportunities = []
    if event:
        scanner = ArbitrageScanner(min_profit=min_profit, min_roi=min_roi)
        opportunities = scanner.scan(event_query=event, state=state.upper() if state else None)

    return TEMPLATES.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "event": event or "",
            "state": state.upper() if state else "",
            "min_profit": min_profit,
            "min_roi": min_roi,
            "opportunities": opportunities,
        },
    )
