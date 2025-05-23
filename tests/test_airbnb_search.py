import pytest
from datetime import datetime
from pages.search_page import SearchPage


@pytest.mark.parametrize("location, check_in, check_out, adults, children", [
    ("Tel Aviv", "2025-07-25", "2025-07-27", 2, 1),
])
def test_airbnb_search(page, location, check_in, check_out, adults, children):
    search_page = SearchPage(page, timeout=10000)

    # 1. Open Airbnb
    search_page.open_homepage()

    # 2. Accept cookie popup if it appears
    # search_page.accept_cookies_if_visible()

    # 3. Enter location
    search_page.enter_location(location)

    # 4. Select check-in and check-out dates
    search_page.select_dates(check_in, check_out)

    # 5. Set number of guests
    search_page.set_guests(adults, children)

    # 6. Submit search
    search_page.submit_search()

    # 7. Wait briefly for page to load
    page.wait_for_timeout(5000)

    # 8. Validate URL contains search params
    print(f"Final URL: {page.url}")
    assert f"checkin={check_in}" in page.url
    assert f"checkout={check_out}" in page.url
    assert f"adults={adults}" in page.url
    assert f"children={children}" in page.url
    assert location.lower().replace(" ", "-") in page.url.lower()

    # 9. Validate UI shows selected search parameters
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
