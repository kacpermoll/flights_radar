from KayakPage.Kayak import Kayak
from time import sleep

bot = Kayak()
bot.start_kayak("KRK", "VLC", "2022-06-01", "2022-06-05")
sleep(5)
bot.page_scrape()
sleep(10)
bot.__exit__()
