from KayakPage.Kayak import Kayak
from time import sleep

bot = Kayak()
bot.land_first_page()
sleep(5)
bot.cheapest_option()
sleep(5)
# bot.load_more()
bot.page_scrape()
bot.__exit__()



