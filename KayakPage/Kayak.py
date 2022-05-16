from selenium import webdriver
import KayakPage.constants as const

class Kayak():
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


    