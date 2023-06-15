from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
link = "https://www.tradingview.com/symbols/XAUUSD/?exchange=OANDA"
data = []
driver.get(link)
wait = WebDriverWait(driver, 10)
fieldnames = ['time', 'price']

with open('C:\\Users\\abdul\\Documents\\stockapp\\price_data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "quotesRow-pAUXADuj")))
    price = ''
    for i in price_element.text.split("\n")[0]:
        if i.isdigit() or i == ".":
            price += i

    if price != '':
        with open('C:\\Users\\abdul\\Documents\\stockapp\\price_data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {"time": datetime.now().strftime('%M:%S'), "price": float(price)}
            csv_writer.writerow(info)
            print(datetime.now().strftime('%M:%S'), price)
    time.sleep(2)
