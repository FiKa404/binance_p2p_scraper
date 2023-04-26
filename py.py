from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import telebot

import time
url = 'https://p2p.binance.com/en/trade/sell/USDT?fiat=EGP'
BOT_TOKEN = '6035784785:AAFORmgTAn1QtobUQKne-Qo84FnXN5puDzw'
sleep = 120

bot = telebot.TeleBot(BOT_TOKEN,parse_mode=None)

@bot.message_handler(commands=['start'])
def subscribe(message):
    bot.reply_to(message, "Please wait....")
    lo()

options = Options()
options.add_argument("--headless")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

def lo():
    while True:    
        all_items = []
        print('> loading page')
        driver.get(url)
        driver.implicitly_wait(12)

        try:
            print('> getting data 1')
            prices = driver.find_elements(By.XPATH, '//div[@class="css-1m1f8hn"]')
            amounts = driver.find_elements(By.XPATH, '//div[@class="css-16w8hmr"]')
            for i in range(len(prices)):
                all_items.append('{}E£  ( {} ) '.format(prices[i].text,amounts[i].text
                                                    .replace('Limit','')
                                                    .replace('\n','')
                                                    .replace('E£','')
                                                    .replace('-',' - ')))

            bot.send_message(2024020468,'USDT/EGP\nBANK TRANSFER *SELL*\n\n'+'\n'.join(all_items),parse_mode='MARKDOWN')
                
        except Exception as e: 
            print(e)

        print('Sleeping for {}s...'.format(sleep))
        time.sleep(sleep)

bot.infinity_polling()