import json
import re
import pytest
from datetime import datetime
from pages.search_page import SearchPage


@pytest.mark.parametrize("location, check_in, check_out, adults, children", [
    ("Tel Aviv", "2025-07-25", "2025-07-27", 2, 1),
])
def test_full_airbnb_booking_flow(page, location, check_in, check_out, adults, children):
    search_page = SearchPage(page, timeout=10000)

    # Step 1: Navigate to Airbnb homepage
    search_page.open_homepage()

    # Step 2: Perform search with location, dates, and guest count
    search_page.enter_location(location)
    search_page.select_dates(check_in, check_out)
    search_page.set_guests(adults, children)
    search_page.submit_search()

    # Step 3: Wait for search results to load and validate URL parameters
    page.wait_for_timeout(5000)
    assert f"checkin={check_in}" in page.url
    assert f"checkout={check_out}" in page.url
    assert f"adults={adults}" in page.url
    assert f"children={children}" in page.url
    assert location.lower().replace(" ", "-") in page.url.lower()

    # Step 4: Validate visible UI elements reflect search input
    check_in_day = str(int(datetime.strptime(check_in, "%Y-%m-%d").day))
    check_out_day = str(int(datetime.strptime(check_out, "%Y-%m-%d").day))
    total_guests = str(adults + children)

    assert page.locator(
        f"//span[text()='Check in / Check out']/following-sibling::div[contains(text(), '{check_in_day}')]"
    ).first.is_visible()

    assert page.locator(
        f"//span[text()='Check in / Check out']/following-sibling::div[contains(text(), '{check_out_day}')]"
    ).first.is_visible()

    assert page.locator(
        f"//span[text()='Guests']/following-sibling::div[contains(text(), '{total_guests}')]"
    ).first.is_visible()

    assert page.locator(
        f"//span[text()='Location']/following-sibling::div[contains(text(), '{location}')]"
    ).first.is_visible()

    # Step 5: Analyze search results and identify cheapest top-rated listing
    cheapest = search_page.analyze_results_and_save_cheapest_top_rated()
    assert cheapest is not None
    assert "price" in cheapest
    assert "rating" in cheapest

    # Step 6: Attempt reservation for the selected listing
    search_page.attempt_reservation(position=cheapest["index"])

    # Step 7: Parse and validate reservation total against expected price
    with open("temp/final_reservation.json") as f:
        reservation = json.load(f)

    def parse_price(text):
        match = re.search(r'[\d,.]+', text.replace(",", ""))
        if not match:
            raise ValueError(f"Could not parse price from: {text}")
        return float(match.group(0))

    reservation_total = parse_price(reservation["total"])
    expected_price = float(cheapest["price"])

    assert abs(expected_price - reservation_total) <= 1, (
        f"Price mismatch: {expected_price} vs {reservation_total}"
    )

'dd'