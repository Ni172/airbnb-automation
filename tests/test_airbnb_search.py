import json
import os

import pytest
from datetime import datetime
from pages.search_page import SearchPage


@pytest.mark.parametrize("location, check_in, check_out, adults, children", [
    ("Tel Aviv", "2025-07-25", "2025-07-27", 2, 1),
])
def test_airbnb_search_and_analyze(page, location, check_in, check_out, adults, children):
    search_page = SearchPage(page, timeout=10000)

    # 1. Open Airbnb homepage
    search_page.open_homepage()

    # 2. Perform search with given inputs
    search_page.enter_location(location)
    search_page.select_dates(check_in, check_out)
    search_page.set_guests(adults, children)
    search_page.submit_search()

    # 3. Wait for results page to load
    page.wait_for_timeout(5000)
    print(f"Final URL: {page.url}")

    # 4. Validate search parameters in URL
    assert f"checkin={check_in}" in page.url
    assert f"checkout={check_out}" in page.url
    assert f"adults={adults}" in page.url
    assert f"children={children}" in page.url
    assert location.lower().replace(" ", "-") in page.url.lower()

    # 5. Validate UI search summary shows correct values
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

    # 6. Analyze listings and save the cheapest among top-rated ones
    cheapest = search_page.analyze_results_and_save_cheapest_top_rated()
    print(f"[Analyze] Cheapest top-rated listing: {cheapest}")

    # 7. Validate analysis result was extracted and saved
    assert cheapest is not None
    assert "price" in cheapest
    assert "rating" in cheapest

    # Step 4: Attempt reservation using index+1 (XPath is 1-based)
    search_page.attempt_reservation(position=cheapest["index"])