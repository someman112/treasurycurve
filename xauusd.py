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
base_link = "https://www.tradingview.com/symbols/"
data = []
previous_price = None
wait = WebDriverWait(driver, 10)


async def handle_client(websocket):
    global previous_price
    connected_clients.add(websocket)
    try:
        symbol = await websocket.recv()
        link = base_link + symbol
        driver.get(link)

        while True:
            dataa = generate_data()

            if dataa != previous_price:
                await websocket.send(str(dataa))
                previous_price = dataa

            try:
                symbol = await asyncio.wait_for(websocket.recv(), timeout=1)
                link = base_link + symbol
                driver.get(link)
            except asyncio.TimeoutError:
                pass

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)


async def start_server():
    server = await websockets.serve(handle_client, "localhost", 8765)

    async with server:
        while True:
            await asyncio.sleep(0.1)
            if connected_clients:
                await asyncio.wait([handle_client(client) for client in connected_clients], timeout=0.1)


def generate_data():
    price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "quotesRow-pAUXADuj")))
    price = ''
    for i in price_element.text.split("\n")[0]:
        if i.isdigit() or i == ".":
            price += i

    if price != '':
        return float(price)


asyncio.get_event_loop().run_until_complete(start_server())
