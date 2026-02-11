from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TicketListing:
    platform: str
    event_id: str
    event_name: str
    city: str
    state: str
    section: str
    row: str
    quantity: int
    price: float
    currency: str = "USD"


@dataclass(slots=True)
class ArbitrageOpportunity:
    event_id: str
    event_name: str
    city: str
    state: str
    section: str
    row: str
    quantity: int
    buy_platform: str
    buy_price: float
    sell_platform: str
    sell_price: float
    estimated_profit: float
    roi: float
