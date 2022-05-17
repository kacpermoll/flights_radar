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

        print(a_travels_l)
        print(b_travels_l)
        # raise SystemExit

        # a_duration = []
        # a_section_names = []
        # for n in a_travels_l:
        #     # Separate the time from the cities
        #     a_section_names.append(''.join(n.split()[2:5]))
        #     a_duration.append(''.join(n.split()[0:2]))
        # b_duration = []
        # b_section_names = []
        # for n in b_travels_l:
        #     # Separate the time from the cities
        #     b_section_names.append(''.join(n.split()[2:5]))
        #     b_duration.append(''.join(n.split()[0:2]))
        # print(a_duration)
        # xp_dates = '//div[@class="section date"]'
        # dates = self.driver.find_elements_by_xpath(xp_dates)
        # dates_list = [value.text for value in dates]
        # a_date_list = dates_list[::2]
        # b_date_list = dates_list[1::2]
        # # Separating the weekday from the day
        # a_day = [value.split()[0] for value in a_date_list]
        # a_weekday = [value.split()[1] for value in a_date_list]
        # b_day = [value.split()[0] for value in b_date_list]
        # b_weekday = [value.split()[1] for value in b_date_list]
        
        # # getting the prices
        # xp_prices = '//a[@class="booking-link"]/span[@class="price option-text"]'
        # prices = self.driver.find_elements_by_xpath(xp_prices)
        # prices_list = [price.text.replace('$','') for price in prices if price.text != '']
        # prices_list = list(map(int, prices_list))

        # # the stops are a big list with one leg on the even index and second leg on odd index
        # xp_stops = '//div[@class="section stops"]/div[1]'
        # stops = self.driver.find_elements_by_xpath(xp_stops)
        # stops_list = [stop.text[0].replace('n','0') for stop in stops]
        # a_stop_list = stops_list[::2]
        # b_stop_list = stops_list[1::2]

        # xp_stops_cities = '//div[@class="section stops"]/div[2]'
        # stops_cities = self.driver.find_elements_by_xpath(xp_stops_cities)
        # stops_cities_list = [stop.text for stop in stops_cities]
        # a_stop_name_list = stops_cities_list[::2]
        # b_stop_name_list = stops_cities_list[1::2]
        
        # # this part gets me the airline company and the departure and arrival times, for both legs
        # xp_schedule = '//div[@class="section times"]'
        # schedules = self.driver.find_elements_by_xpath(xp_schedule)
        # hours_list = []
        # carrier_list = []
        # for schedule in schedules:
        #     hours_list.append(schedule.text.split('\n')[0])
        #     carrier_list.append(schedule.text.split('\n')[1])
        # # split the hours and carriers, between a and b legs
        # a_hours = hours_list[::2]
        # a_carrier = carrier_list[::2]
        # b_hours = hours_list[1::2]
        # b_carrier = carrier_list[1::2]

        
        # cols = (['Out Day', 'Out Time', 'Out Weekday', 'Out Airline', 'Out Cities', 'Out Duration', 'Out Stops', 'Out Stop Cities',
        #         'Return Day', 'Return Time', 'Return Weekday', 'Return Airline', 'Return Cities', 'Return Duration', 'Return Stops', 'Return Stop Cities',
        #         'Price'])

        # flights_df = pd.DataFrame({'Out Day': a_day,
        #                         'Out Weekday': a_weekday,
        #                         'Out Duration': a_duration,
        #                         'Out Cities': a_section_names,
        #                         'Return Day': b_day,
        #                         'Return Weekday': b_weekday,
        #                         'Return Duration': b_duration,
        #                         'Return Cities': b_section_names,
        #                         'Out Stops': a_stop_list,
        #                         'Out Stop Cities': a_stop_name_list,
        #                         'Return Stops': b_stop_list,
        #                         'Return Stop Cities': b_stop_name_list,
        #                         'Out Time': a_hours,
        #                         'Out Airline': a_carrier,
        #                         'Return Time': b_hours,
        #                         'Return Airline': b_carrier,                           
        #                         'Price': prices_list})[cols]
        
        # flights_df['timestamp'] = strftime("%Y%m%d-%H%M") # so we can know when it was scraped
        # print(flights_df)
        # return flights_df