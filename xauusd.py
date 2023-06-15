import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import websockets

connected_clients = set()

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
link = "https://www.tradingview.com/symbols/XAUUSD/?exchange=OANDA"
data = []
previous_price = None
driver.get(link)
wait = WebDriverWait(driver, 10)


async def handle_client(websocket, path):
    global previous_price
    connected_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # Adjust the sleep duration as needed
            data = generate_data()
            if data != previous_price:
                await websocket.send(str(data))
                previous_price = data
    finally:
        connected_clients.remove(websocket)


async def start_server():
    server = await websockets.serve(handle_client, "localhost", 8765)

    async with server:
        await server.serve_forever()


def generate_data():
    price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "quotesRow-pAUXADuj")))
    price = ''
    for i in price_element.text.split("\n")[0]:
        if i.isdigit() or i == ".":
            price += i

    if price != '':
        return float(price)


asyncio.get_event_loop().run_until_complete(start_server())
