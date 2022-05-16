from selenium import webdriver
import Bing_Travel.constants as const

class BingTravel():
    def __init__(self, teardown=True, path_to_driver=const.PATH_TO_DRIVER):
        self.driver = webdriver.Edge(path_to_driver)
        self.teardown = teardown
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
 

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(const.BASE_URL)

    def accept_cookies(self):
        try:
            cookies = self.driver.find_element_by_css_selector(
            'button[id="bnp_btn_accept"]'
            )
            cookies.click()
        except:
            print("No such button")

    
    def enter_departure(self):
        departure = self.driver.find_element_by_css_selector(
            'input[placeholder="Lot z?"]'
        )
        departure.clear()
        departure.send_keys('Warszawa')

    def choose_deprature_airport(self):
        departure_airport = self.driver.find_element_by_css_selector(
            'li[id="downshift-3-item-0"]'
        )
        departure_airport.click()
    