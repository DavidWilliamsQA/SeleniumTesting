from booking.booking import Booking
from booking.scrapping import Scrapping
from time import sleep
from random import randint

try:
    with Booking() as bot:
        bot.start_booking()
        bot.handle_cookies()
        bot.change_currency("USD")
        bot.select_place_to_go("Frankfurt")
        bot.select_date("2022-04-12")
        bot.select_date("2022-04-18")
        bot.select_adults(3)
        bot.click_search()
        bot.apply_filtrations()
        sleep(5)
        bot.begin_scrapping()

except Exception as e:
    if "in PATH" in str(e):
        print(
            "You are trying to run the bot from command line \n"
            "Please add to PATH your Selenium Drivers \n"
            "Windows: \n"
            "    set PATH=%PATH%;C:path-to-your-folder \n \n"
            "Linux: \n"
            "    PATH=$PATH:/path/toyour/folder/ \n"
        )
    else:
        raise
