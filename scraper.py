from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import telebot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import psutil
from multiprocessing import Process
import time

#Put your bot token here
BOT_TOKEN = '##########'
#Chat id that the data will be sent to (If it is private chat you have to put it's id
#If the chat is channel or group you can use both id or username)
chat_id = 0000000
#Sleeping time after each scrape in seconds
sleep = 560
#Fiat you want with USDT
fiat = 'egp'
url = f'https://p2p.binance.com/en/trade/sell/USDT?fiat={fiat}'
bot = telebot.TeleBot(BOT_TOKEN)


options = Options()
#To decrease the huge logs we are getting when run the app
options.add_argument("--log-level=3") 

# UnComment the next line if you want to run the browser in headless mode (run invisible)
# options.add_argument("--headless")
s=Service(ChromeDriverManager().install())


def worker():
    while True:
      print('> loading page')
      driver = webdriver.Chrome(service=s,options=options)
      wait = WebDriverWait(driver, 10)
      driver.get(url)
      time.sleep(20)
      fiat_select = driver.find_element(By.XPATH,'//*[@id="C2Cfiatfilter_searchbox_fiat"]/div[1]/div/div')
      fiat_select.click()
      time.sleep(1)
      fiat_field = fiat_select.find_element(By.XPATH,'//*[@id="C2Cfiatfilter_searchbox_fiat"]/div[2]/div/div/input')
      fiat_field.send_keys(fiat)
      time.sleep(2)
      fiat_field.send_keys(Keys.ENTER)
      time.sleep(10)
      all_items = []  
      try:
          print('> scarping data')
          prices = driver.find_elements(By.XPATH, '//div[@class="css-1m1f8hn"]')
          amounts = driver.find_elements(By.XPATH, '//div[@class="css-16w8hmr"]')
          for i in range(len(prices)):
              all_items.append('{}E£  ( {} ) '.format(prices[i].text,amounts[i].text
                                                  .replace('Limit','')
                                                  .replace('\n','')
                                                  .replace('E£','')
                                                  .replace('-',' - ')))

          print('> sending data')
          bot.send_message(chat_id,'EGP/USDT\nALL PAYMENTS *SELL*\n\n'+'\n'.join(all_items),parse_mode='MARKDOWN')
              
      except Exception as e:           
          print(e)

      all_items.clear()
      print(f'Sleeping for {sleep}s...')
      time.sleep(sleep)


if __name__ == '__main__':
  p1 = Process(target=worker)
    # To start the process when the app run
  p1.start()
    # To control the process suspend or resume it
  p = psutil.Process(p1.pid)

#To resume the process using 'start' command for the bot in TG
  @bot.message_handler(commands=['start'])
  def start(message):
    bot.reply_to(message, "Started....")
    p.resume()  

#To suspend the process using 'stop' command for the bot in TG
  @bot.message_handler(commands=['stop'])
  def stop(message):
    p.suspend()
    bot.reply_to(message, "Stopped...")

    
  bot.infinity_polling()
  
