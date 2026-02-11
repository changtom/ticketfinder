from ticketfinder.models import TicketListing
from ticketfinder.scanner import ArbitrageScanner


class FakeClient:
    def __init__(self, name: str, listings: list[TicketListing]) -> None:
        self.name = name
        self._listings = listings

    def fetch_listings(self, event_query: str, state: str | None = None) -> list[TicketListing]:
        if state:
            return [item for item in self._listings if item.state == state]
        return self._listings


def test_finds_profitable_direction_between_platforms() -> None:
    base = dict(
        event_id="event-1",
        event_name="Test Event",
        city="Boston",
        state="MA",
        section="101",
        row="A",
        quantity=2,
    )
    buy_listing = TicketListing(platform="ticketmaster", price=80.0, **base)
    sell_listing = TicketListing(platform="stubhub", price=135.0, **base)

    scanner = ArbitrageScanner(
        min_profit=1,
        min_roi=0,
        buy_fee_rate=0.10,
        sell_fee_rate=0.10,
        clients=[FakeClient("tm", [buy_listing]), FakeClient("sh", [sell_listing])],
    )

    opportunities = scanner.scan("Test Event")

    assert len(opportunities) == 1
    assert opportunities[0].buy_platform == "ticketmaster"
    assert opportunities[0].sell_platform == "stubhub"
    assert opportunities[0].estimated_profit > 0


def test_state_filter_applies() -> None:
    ny_listing = TicketListing(
        platform="ticketmaster",
        event_id="event-2",
        event_name="State Test",
        city="New York",
        state="NY",
        section="201",
        row="B",
        quantity=2,
        price=100,
    )
    ca_listing = TicketListing(
        platform="stubhub",
        event_id="event-2",
        event_name="State Test",
        city="Los Angeles",
        state="CA",
        section="201",
        row="B",
        quantity=2,
        price=130,
    )

    scanner = ArbitrageScanner(clients=[FakeClient("tm", [ny_listing]), FakeClient("sh", [ca_listing])])

    opportunities = scanner.scan("State Test", state="NY")

    assert opportunities == []
