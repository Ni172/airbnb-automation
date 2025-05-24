# pages/search_page.py
from datetime import datetime
import json
import os
import re

from pages.base_page import BasePage


class SearchPage(BasePage):
    def open_homepage(self):
        self.goto("https://www.airbnb.com/")

    def accept_cookies_if_visible(self):
        try:
            self.click("button:has-text('Accept')")
        except:
            pass  # Optional if cookie dialog doesn't appear

    def enter_location(self, location: str):
        self.click("[data-testid='structured-search-input-field-query']")
        self.fill("input", location)
        self.page.keyboard.press("Enter")

    from datetime import datetime

    from datetime import datetime

    def select_dates(self, check_in: str, check_out: str):
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

        # Open the date picker
        # self.click("//button[@data-testid='structured-search-input-field-dates-button']")

        # Navigate and select check-in date
        self._go_to_month(check_in_date)
        self.click(f"//button[@data-state--date-string='{check_in_date.strftime('%Y-%m-%d')}']")

        # Navigate and select check-out date
        self._go_to_month(check_out_date)
        self.click(f"//button[@data-state--date-string='{check_out_date.strftime('%Y-%m-%d')}']")

    def _go_to_month(self, target_date: datetime):
        target_month_year = target_date.strftime("%B %Y")

        for _ in range(12):  # prevent infinite loops
            # Look for visible calendar month labels (e.g., "June 2025")
            self.page.wait_for_timeout(500)  # wait briefly for UI to update
            headers = self.page.locator('//div[@role="tabpanel"]//h2')
            texts = headers.all_text_contents()

            if any(target_month_year in t for t in texts):
                print(f"Found month: {target_month_year}")
                return

            # Click next month button (right arrow)
            self.page.locator(
                '//button[contains(@aria-label,"Move forward to switch to the next month.")]').first.click()

        raise Exception(f"Month {target_month_year} not found")

    def set_guests(self, adults: int, children: int):
        # Open the guest selector using visible text
        self.click("//div[contains(text(), 'Who')]")

        # Increase adults (starts at 1)
        for _ in range(adults):
            self.click_first("//div[@id='stepper-adults']//button[@data-testid='stepper-adults-increase-button']")

        # Increase children (starts at 0)
        for _ in range(children):
            self.click_first("//div[@id='stepper-children']//button[@data-testid='stepper-children-increase-button']")

    def submit_search(self):
        self.click("//div[normalize-space(text())='Search']")

    def analyze_results_and_save_cheapest_top_rated(self):
        print("[Analyze] Analyzing search results...")

        # Wait for listings to load
        self.page.wait_for_selector('//div[contains(@itemprop, "itemListElement")]', timeout=10000)
        listings = self.page.locator('//div[contains(@itemprop, "itemListElement")]')
        count = listings.count()
        print(f"[Analyze] Found {count} listings")

        results = []

        for i in range(count):
            try:
                card = listings.nth(i)
                if not card.is_visible():
                    print(f"[Analyze] Skipping invisible listing {i}")
                    continue

                # Extract price using regex from full card text
                card_text = card.inner_text()
                price_match = re.search(r'₪[\d,]+', card_text)
                if not price_match:
                    raise ValueError(f"No price found in: {card_text}")
                price_str = price_match.group(0).replace("₪", "").replace(",", "")
                price = int(price_str)

                # Extract rating using regex
                rating_match = re.search(r'(\d\.\d)\s*\(\d+\)', card_text)
                if not rating_match:
                    raise ValueError(f"No rating found in: {card_text}")
                rating = float(rating_match.group(1))

                results.append({
                    "index": i,
                    "price": price,
                    "rating": rating,
                    "text": card_text
                })

            except Exception as e:
                print(f"[Analyze] Skipping listing {i}: {e}")
                continue

        if not results:
            raise Exception("No listings with both price and rating found")

        max_rating = max(r["rating"] for r in results)
        top_rated = [r for r in results if r["rating"] == max_rating]
        cheapest = min(top_rated, key=lambda r: r["price"])

        print(f"[Analyze] Cheapest top-rated: ₪{cheapest['price']} | Rating: {cheapest['rating']}")

        # Save to temp folder
        os.makedirs("temp", exist_ok=True)
        with open("temp/cheapest_top_rated.json", "w") as f:
            json.dump(cheapest, f, indent=2)

        return cheapest

    def attempt_reservation(self, position):
        print("[Reserve] Opening listing and attempting reservation...")

        # Step 1: Click the first listing and switch to new page (popup)
        with self.page.expect_popup() as popup_info:
            self.page.locator(
                f'(//div[contains(@itemprop, "itemListElement")])[{position}]//div[@data-testid="card-container"]'
            ).first.click()

        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")

        # Step 2: Close login/signup prompt (if shown)
        try:
            popup.get_by_role("button", name="Close").click()
            print("[Reserve] Closed login popup")
        except:
            print("[Reserve] No close button appeared")

        # Step 3: Click "Reserve"
        popup.get_by_role("button", name="Reserve").click()

        # Step 4: Select country code (e.g., +972 for Israel)
        try:
            import re
            popup.locator("div").filter(has_text=re.compile(r"^\+972$")).first.click()
            print("[Reserve] Selected country prefix +972")
        except:
            print("[Reserve] No prefix selector needed")

        # Step 5: Fill phone number
        popup.get_by_test_id("login-signup-phonenumber").fill("0523428437")
        popup.get_by_test_id("signup-login-submit-btn").click()

        # Step 6: Confirm phone prompt (if shown)
        try:
            popup.get_by_test_id("modal-container").get_by_text("Confirm your number").click()
            print("[Reserve] Clicked confirm prompt")
        except:
            print("[Reserve] Confirm prompt not visible")

        # Step 7: (Optional) Extract and save final reservation summary
        summary = {
            "url": popup.url,
            "status": "reservation started",
            "phone": "0523428437"
        }

        os.makedirs("temp", exist_ok=True)
        with open("temp/final_reservation.json", "w") as f:
            json.dump(summary, f, indent=2)

        print("[Reserve] Reservation attempt logged.")
