# pages/base_page.py

from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.default_timeout = timeout

    def goto(self, url: str):
        """Navigate to a URL and wait for the network to be idle."""
        self.page.goto(url, wait_until="networkidle")

    def get_text(self, selector: str) -> str:
        """Get inner text of the first matching element."""
        locator = self.page.locator(selector).first
        locator.wait_for(timeout=self.default_timeout, state="visible")
        return locator.inner_text()

    def click(self, selector: str):
        """Click the (single expected) element matched by the selector."""
        locator = self.page.locator(selector)
        locator.wait_for(timeout=self.default_timeout, state="visible")
        locator.scroll_into_view_if_needed()
        locator.click()

    def click_first(self, selector: str):
        """Click only the first element that matches the selector."""
        locator = self.page.locator(selector).first
        locator.wait_for(timeout=self.default_timeout, state="visible")
        locator.scroll_into_view_if_needed()
        locator.click()

    def fill(self, selector: str, text: str):
        """Fill the first visible input element with text."""
        locator = self.page.locator(selector).first
        locator.wait_for(timeout=self.default_timeout, state="visible")
        locator.fill(text)

    def wait_for_selector(self, selector: str):
        """Explicitly wait for a selector to appear (optional legacy use)."""
        self.page.wait_for_selector(selector, timeout=self.default_timeout)

    def get_all_texts(self, selector: str) -> list[str]:
        """Wait for at least one element to be visible and return all inner texts."""
        self.page.wait_for_selector(selector, timeout=self.default_timeout)
        locator = self.page.locator(selector)
        return locator.all_text_contents()

    def get_first_text(self, selector: str, popup=None) -> str:
        """Wait for the first matching element to be visible and return its text."""
        target = popup if popup else self.page
        locator = target.locator(selector).first
        locator.wait_for(timeout=self.default_timeout, state="visible")
        return locator.inner_text()

    def is_element_visible(self, selector: str) -> bool:
        """
        Check if the element matching the given selector is visible on the page.

        This waits until the first matched element is visible using the default timeout,
        then scrolls it into view and returns its visibility status.

        Args:
            selector (str): A CSS or XPath selector string.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        locator = self.page.locator(selector).first
        try:
            locator.wait_for(timeout=self.default_timeout, state="visible")
            locator.scroll_into_view_if_needed()
            return locator.is_visible()
        except:
            return False
