# pages/search_page.py
from datetime import datetime

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
