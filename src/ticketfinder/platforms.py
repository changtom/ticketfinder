from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Iterable

import requests

from .models import TicketListing


class PlatformClient(ABC):
    name: str

    @abstractmethod
    def fetch_listings(self, event_query: str, state: str | None = None) -> list[TicketListing]:
        raise NotImplementedError


class SeatGeekClient(PlatformClient):
    name = "seatgeek"

    def __init__(self, client_id: str | None = None) -> None:
        self.client_id = client_id or os.getenv("SEATGEEK_CLIENT_ID")

    def fetch_listings(self, event_query: str, state: str | None = None) -> list[TicketListing]:
        if not self.client_id:
            return _fallback_listings(self.name, event_query, state)

        params = {
            "q": event_query,
            "per_page": 10,
            "client_id": self.client_id,
        }
        response = requests.get("https://api.seatgeek.com/2/events", params=params, timeout=15)
        response.raise_for_status()
        events = response.json().get("events", [])

        listings: list[TicketListing] = []
        for event in events:
            venue = event.get("venue") or {}
            if state and venue.get("state") != state:
                continue
            listing_count = max(1, int(event.get("stats", {}).get("listing_count") or 1))
            avg_price = float(event.get("stats", {}).get("average_price") or 80)
            listings.append(
                TicketListing(
                    platform=self.name,
                    event_id=f"sg-{event['id']}",
                    event_name=event.get("title", "Unknown Event"),
                    city=venue.get("city", "Unknown"),
                    state=venue.get("state", "NA"),
                    section="GEN",
                    row="GA",
                    quantity=min(listing_count, 4),
                    price=avg_price,
                )
            )

        return listings or _fallback_listings(self.name, event_query, state)


class TicketmasterClient(PlatformClient):
    name = "ticketmaster"

    def fetch_listings(self, event_query: str, state: str | None = None) -> list[TicketListing]:
        return _fallback_listings(self.name, event_query, state)


class StubHubClient(PlatformClient):
    name = "stubhub"

    def fetch_listings(self, event_query: str, state: str | None = None) -> list[TicketListing]:
        return _fallback_listings(self.name, event_query, state)


def _fallback_listings(platform: str, event_query: str, state: str | None) -> list[TicketListing]:
    price_offsets = {"ticketmaster": 0.82, "stubhub": 1.38, "seatgeek": 1.0}
    factor = price_offsets.get(platform, 1.0)
    sample_pool: Iterable[TicketListing] = (
        TicketListing(platform=platform, event_id=f"{event_query.lower()}-1", event_name=f"{event_query} Live", city="New York", state="NY", section="101", row="A", quantity=2, price=round(150.0 * factor, 2)),
        TicketListing(platform=platform, event_id=f"{event_query.lower()}-2", event_name=f"{event_query} Live", city="Los Angeles", state="CA", section="202", row="F", quantity=2, price=round(95.0 * factor, 2)),
        TicketListing(platform=platform, event_id=f"{event_query.lower()}-3", event_name=f"{event_query} Tour", city="Chicago", state="IL", section="310", row="C", quantity=4, price=round(72.0 * factor, 2)),
    )
    if state:
        return [listing for listing in sample_pool if listing.state == state]
    return list(sample_pool)
