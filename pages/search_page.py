import json
import os
import re
from datetime import datetime

from pages.base_page import BasePage


class SearchPage(BasePage):
    def open_homepage(self):
        # Open Airbnb homepage
        self.goto("https://www.airbnb.com/")

    def enter_location(self, location: str):
        # Enter a search location in the search input
        self.click("[data-testid='structured-search-input-field-query']")
        self.fill("input", location)
        self.page.keyboard.press("Enter")

    def select_dates(self, check_in: str, check_out: str):
        # Select check-in and check-out dates from the calendar
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        self._go_to_month(check_in_date)
        self.click(f"//button[@data-state--date-string='{check_in_date.strftime('%Y-%m-%d')}']")
        self._go_to_month(check_out_date)
        self.click(f"//button[@data-state--date-string='{check_out_date.strftime('%Y-%m-%d')}']")

    def _go_to_month(self, target_date: datetime):
        # Navigate the calendar to reach the desired month
        target_month_year = target_date.strftime("%B %Y")
        for _ in range(12):
            self.page.wait_for_timeout(500)
            headers = self.page.locator('//div[@role="tabpanel"]//h2')
            texts = headers.all_text_contents()
            if any(target_month_year in t for t in texts):
                return
            self.page.locator('//button[contains(@aria-label,"Move forward")]').first.click()
        raise Exception(f"Month {target_month_year} not found")

    def set_guests(self, adults: int, children: int):
        # Set the number of adults and children guests
        self.click("//div[contains(text(), 'Who')]")
        for _ in range(adults):
            self.click_first("//div[@id='stepper-adults']//button[@data-testid='stepper-adults-increase-button']")
        for _ in range(children):
            self.click_first("//div[@id='stepper-children']//button[@data-testid='stepper-children-increase-button']")

    def submit_search(self):
        # Submit the search query
        self.click("//div[normalize-space(text())='Search']")

    def analyze_results_and_save_cheapest_top_rated(self):
        # Analyze search results and save the cheapest top-rated listing to a JSON file
        self.page.wait_for_selector('//div[contains(@itemprop, "itemListElement")]', timeout=10000)
        listings = self.page.locator('//div[contains(@itemprop, "itemListElement")]')
        results = [self._extract_listing_info(listings.nth(i), i) for i in range(listings.count())]
        results = [r for r in results if r]

        if not results:
            raise Exception("No valid listings found")

        max_rating = max(r["rating"] for r in results)
        top_rated = [r for r in results if r["rating"] == max_rating]
        cheapest = min(top_rated, key=lambda r: r["price"])

        os.makedirs("temp", exist_ok=True)
        with open("temp/cheapest_top_rated.json", "w") as f:
            json.dump(cheapest, f, indent=2)

        return cheapest

    def _extract_listing_info(self, card, index):
        # Extract price and rating info for a single listing
        try:
            if not card.is_visible():
                return None
            text = card.inner_text()
            prices = re.findall(r'₪[\d,]+', text)
            if not prices:
                return None
            price = int(prices[-1].replace("₪", "").replace(",", ""))
            rating_match = re.search(r'(\d\.\d)\s*\(\d+\)', text)
            if not rating_match:
                return None
            rating = float(rating_match.group(1))
            return {"index": index, "price": price, "rating": rating, "text": text}
        except:
            return None

    def attempt_reservation(self, position: int, phonenumber='123456789'):
        # Attempt to reserve a specific listing and extract reservation summary
        with self.page.expect_popup() as popup_info:
            self.page.locator(
                f'(//div[contains(@itemprop, "itemListElement")])[{position + 1}]//div[@data-testid="card-container"]'
            ).first.click()

        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        self._close_optional_popup(popup)
        popup.get_by_role("button", name="Reserve").click()
        self._select_country_code(popup)
        popup.get_by_test_id("login-signup-phonenumber").fill(phonenumber)
        summary = self._extract_reservation_summary(popup, phonenumber)

        os.makedirs("temp", exist_ok=True)
        with open("temp/final_reservation.json", "w") as f:
            json.dump(summary, f, indent=2)

    def _close_optional_popup(self, popup):
        # Attempt to close any optional modal popup
        try:
            popup.get_by_role("button", name="Close").click()
        except:
            pass

    def _select_country_code(self, popup):
        # Select +972 country code from the dropdown
        try:
            popup.locator("div").filter(has_text=re.compile(r"^\+972$")).first.click()
        except:
            pass

    def _extract_reservation_summary(self, popup, phonenumber):
        # Extract pricing details from the reservation summary screen
        summary = {
            "url": popup.url,
            "status": "reservation started",
            "phone": phonenumber
        }
        try:
            summary["price_per_night_block"] = popup.locator(
                '//div[contains(text(),"x") and contains(text(),"night")]'
            ).first.inner_text()
            summary["price_subtotal"] = popup.locator(
                '//div[contains(text(),"x")]/following-sibling::div'
            ).first.inner_text()
            summary["discount"] = popup.locator(
                '//div[contains(@data-testid,"DISCOUNT")]/div'
            ).first.inner_text()
        except:
            summary["discount"] = "N/A"
        summary["service_fee"] = popup.locator(
            '//div[contains(@data-testid,"AIRBNB_GUEST_FEE")]/span'
        ).first.inner_text()
        summary["total"] = popup.locator(
            '//div[contains(text(),"Total")]/following-sibling::div'
        ).first.inner_text()
        return summary
