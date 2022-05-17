from selenium import webdriver
import KayakPage.constants as const
from random import randint
from time import sleep, strftime
import pandas as pd


class Kayak():
    def __init__(self, teardown=True, path_to_driver=const.PATH_TO_DRIVER):
        self.driver = webdriver.Chrome(path_to_driver)
        self.teardown = teardown
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
 

    def __exit__(self):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(const.BASE_URL)

    # Chose the cheapest options
    def cheapest_option(self):
        cheap_result = '//a[@data-code="price"]'
        print("Before choice")
        self.driver.find_element_by_xpath(cheap_result).click()
        print("After choice")
    # Load more results to maximize the scraping
    def load_more(self):
        try:
            more_results = '//a[@class = "moreButton"]'
            self.driver.find_element_by_xpath(more_results).click()
            # Printing these notes during the program helps me quickly check what it is doing
            print('sleeping.....')
            sleep(randint(45,60))
        except:
            pass

    def page_scrape(self):
        """
        This function takes care of scraping page and creating a dataframe
        """
        """
        a_(...) - outbound flight
        b_(...) - inbound flight
        (...)_l - list
        (...)_t - temporary
        """       

        # Scraping all trips without prices
        all_travels = self.driver.find_elements_by_xpath('//*[@class="container"]')
        all_travels_l = [value.text for value in all_travels]

        # Dividing the trips into outbound and inbound
        a_travels_l = []
        b_travels_l = []
        [a_travels_l.append(n.split('\n')) for n in all_travels_l[::2]]
        [b_travels_l.append(n.split('\n')) for n in all_travels_l[1::2]]

        if len(a_travels_l) != len(b_travels_l):
            print("Error: The number of outbound and inbound trips is not equal")
            return

        # Deleting element which contains such value: " - "
        for n in range(len(a_travels_l)):
            del a_travels_l[n][3]
            del b_travels_l[n][3]

        # Merging elements which contain information about stopover (change)
        for n in range(len(a_travels_l)):
            if len(a_travels_l[n]) > 6:
                a_travels_l[n][4] = " ".join(a_travels_l[n][4:6])
                del a_travels_l[n][5]

            if len(b_travels_l[n]) > 6:
                b_travels_l[n][4] = " ".join(b_travels_l[n][4:6])
                del b_travels_l[n][5]

        # Scraping prices
        price = self.driver.find_elements_by_xpath('//*[@class="multibook-dropdown"]')
        price_l_t = [value.text for value in price]
        
        # Since prices are scraped with unnecesary information, 
        # we need to delete it and only keep the price that is first in each element
        price_l = []
        for n in price_l_t:
            price_l.append(n.split()[0])
       

        out_day, out_departure, out_arrival, out_departure_airport, out_arrival_airport, out_stops, out_duration = [], [], [], [], [], [], []
        return_day, return_departure, return_arrival, return_departure_airport, return_arrival_airport, return_stops, return_duration = [], [], [], [], [], [], []
        for n in range(len(a_travels_l)):
            out_day.append(a_travels_l[n][0][:-1])
            out_departure.append(a_travels_l[n][1].split(' – ')[0])
            out_arrival.append(a_travels_l[n][1].split(' – ')[1])
            out_departure_airport.append(a_travels_l[n][2])
            out_arrival_airport.append(a_travels_l[n][3])
            out_stops.append(a_travels_l[n][4])
            out_duration.append(a_travels_l[n][5])

            return_day.append(b_travels_l[n][0][:-1])
            return_departure.append(b_travels_l[n][1].split(' – ')[0])
            return_arrival.append(b_travels_l[n][1].split(' – ')[1])
            return_departure_airport.append(b_travels_l[n][2])
            return_arrival_airport.append(b_travels_l[n][3])
            return_stops.append(b_travels_l[n][4])
            return_duration.append(b_travels_l[n][5])

        # Creating a dataframe from the scraped data
        cols = (['Out Day', 'Out Departure', 'Out Arrival', 'Out Departure Airport', 'Out Arrival Airport', 'Out Stops', 'Out Duration',
                'Return Day', 'Return Departure', 'Return Arrival', 'Return Departure Airport', 'Return Arrival Airport', 'Return Stops', 'Return Duration', 
                'Price'])

        flights_df = pd.DataFrame({'Out Day': out_day,
                                    'Out Departure': out_departure,
                                    'Out Arrival': out_arrival,
                                    'Out Departure Airport': out_departure_airport,
                                    'Out Arrival Airport': out_arrival_airport,
                                    'Out Stops': out_stops,
                                    'Out Duration': out_duration,
                                    'Return Day': return_day,
                                    'Return Departure': return_departure,
                                    'Return Arrival': return_arrival,
                                    'Return Departure Airport': return_departure_airport,
                                    'Return Arrival Airport': return_arrival_airport,
                                    'Return Stops': return_stops,
                                    'Return Duration': return_duration,
                                    'Price': price_l})[cols]

        # Adding a column with the date of scraping
        flights_df['timestamp'] = strftime("%Y-%m-%d %H:%M") 
        flights_df.to_excel("output.xlsx", index=False)  
