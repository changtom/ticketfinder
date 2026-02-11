from fastapi.testclient import TestClient

from ticketfinder.web import app


client = TestClient(app)


def test_home_page_renders() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "TicketFinder" in response.text


def test_scan_query_renders_results_section() -> None:
    response = client.get("/", params={"event": "Taylor Swift"})

    assert response.status_code == 200
    assert "Found" in response.text or "No opportunities found" in response.text
