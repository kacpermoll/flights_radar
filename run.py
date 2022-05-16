from Bing_Travel.BingTravel import BingTravel
import time

bot = BingTravel()
bot.land_first_page()
bot.accept_cookies()
bot.enter_departure()
bot.choose_deprature_airport()

time.sleep(5)
bot.driver.quit()



