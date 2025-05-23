import pytest
from pages.search_page import SearchPage


@pytest.mark.parametrize("location, check_in, check_out, adults, children", [
    ("Tel Aviv", "2025-07-25", "2025-07-27", 2, 1),
])
def test_airbnb_search(page, location, check_in, check_out, adults, children):
    search_page = SearchPage(page, 10000)

    # 1. Open Airbnb
    search_page.open_homepage()

    # 2. Accept cookie popup if it appears
    # search_page.accept_cookies_if_visible()

    # 3. Enter location
    search_page.enter_location(location)

    # 4. Select dates (must adjust to actual datepicker format on site)
    search_page.select_dates(check_in, check_out)

    # 5. Set number of guests
    search_page.set_guests(adults, children)

    # 6. Submit search
    search_page.submit_search()

    # 7. Wait for results to load (very basic check)
    page.wait_for_timeout(5000)  # allow time for page to load

    # 8. Validate the location appears in the URL
    assert "Tel-Aviv" in page.url or "tel-aviv" in page.url.lower()

    print("\nSearch page reached successfully.")
    print(f"Final URL: {page.url}")
