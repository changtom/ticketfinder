from __future__ import annotations

from collections import defaultdict
from itertools import combinations

from .models import ArbitrageOpportunity, TicketListing
from .platforms import PlatformClient, SeatGeekClient, StubHubClient, TicketmasterClient


class ArbitrageScanner:
    def __init__(
        self,
        buy_fee_rate: float = 0.12,
        sell_fee_rate: float = 0.15,
        min_profit: float = 15.0,
        min_roi: float = 0.08,
        clients: list[PlatformClient] | None = None,
    ) -> None:
        self.buy_fee_rate = buy_fee_rate
        self.sell_fee_rate = sell_fee_rate
        self.min_profit = min_profit
        self.min_roi = min_roi
        self.clients = clients or [TicketmasterClient(), StubHubClient(), SeatGeekClient()]

    def scan(self, event_query: str, state: str | None = None) -> list[ArbitrageOpportunity]:
        listings = self._collect_listings(event_query=event_query, state=state)
        opportunities: list[ArbitrageOpportunity] = []

        grouped: dict[tuple[str, str, str, str], list[TicketListing]] = defaultdict(list)
        for listing in listings:
            key = (listing.event_name, listing.city, listing.section, listing.row)
            grouped[key].append(listing)

        for (_, city, section, row), group in grouped.items():
            if len(group) < 2:
                continue
            for left, right in combinations(group, 2):
                opportunities.extend(self._evaluate_pair(left, right, city, section, row))

        return sorted(opportunities, key=lambda item: item.estimated_profit, reverse=True)

    def _collect_listings(self, event_query: str, state: str | None = None) -> list[TicketListing]:
        listings: list[TicketListing] = []
        for client in self.clients:
            listings.extend(client.fetch_listings(event_query=event_query, state=state))
        return listings

    def _evaluate_pair(
        self,
        first: TicketListing,
        second: TicketListing,
        city: str,
        section: str,
        row: str,
    ) -> list[ArbitrageOpportunity]:
        opportunities: list[ArbitrageOpportunity] = []
        if first.platform == second.platform:
            return opportunities

        opportunities.extend(self._try_direction(first, second, city, section, row))
        opportunities.extend(self._try_direction(second, first, city, section, row))
        return opportunities

    def _try_direction(
        self,
        buy: TicketListing,
        sell: TicketListing,
        city: str,
        section: str,
        row: str,
    ) -> list[ArbitrageOpportunity]:
        quantity = min(buy.quantity, sell.quantity)
        gross_cost = buy.price * quantity
        gross_revenue = sell.price * quantity
        total_cost = gross_cost * (1 + self.buy_fee_rate)
        net_revenue = gross_revenue * (1 - self.sell_fee_rate)
        profit = net_revenue - total_cost

        if total_cost <= 0:
            return []

        roi = profit / total_cost
        if profit < self.min_profit or roi < self.min_roi:
            return []

        return [
            ArbitrageOpportunity(
                event_id=buy.event_id,
                event_name=buy.event_name,
                city=city,
                state=buy.state,
                section=section,
                row=row,
                quantity=quantity,
                buy_platform=buy.platform,
                buy_price=buy.price,
                sell_platform=sell.platform,
                sell_price=sell.price,
                estimated_profit=round(profit, 2),
                roi=round(roi, 4),
            )
        ]
