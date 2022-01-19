from selenium import webdriver
import os
import booking.constants as const
from selenium.common.exceptions import NoSuchElementException
from booking.booking_filtartion import BookingFiltration
from booking.scrapping import Scrapping


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r";C:/SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(5)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def start_booking(self):
        self.get(const.BASE_URL)

    def handle_cookies(self):
        cookies_decline_button = self.find_element_by_css_selector(
            'button[id="onetrust-accept-btn-handler"]'
        )
        cookies_decline_button.click()

    def change_currency(self, currency=None):
        currency_element = self.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element_by_id("ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element_by_css_selector('li[data-i="0"]')
        first_result.click()

    def select_date(self, date):
        next_arrow = self.find_element_by_css_selector(
            'div[data-bui-ref="calendar-next"]'
        )
        while True:
            try:
                self.find_element_by_css_selector(f'td[data-date="{date}"]')
                self.find_element_by_css_selector(f'td[data-date="{date}"]').click()
                break
            except NoSuchElementException:
                next_arrow.click()

    def select_adults(self, count=1):
        selection_element = self.find_element_by_id("xp__guests__toggle")
        selection_element.click()

        while True:
            decerease_adult_element = self.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            )
            decerease_adult_element.click()

            adults_value_element = self.find_element_by_id("group_adults")
            adults_value = adults_value_element.get_attribute("value")

            if int(adults_value) == 1:
                break

        increase_button_element = self.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
        )

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element_by_css_selector('button[type="submit"]')
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        filtration.sort_price_lowest_first()

    def get_page_source(self):
        strPageSource = self.page_source
        return strPageSource

    def begin_scrapping(self):
        source = self.get_page_source()
        scrapping = Scrapping()
        scrapping.execute(source)
