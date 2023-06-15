import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import numpy as np
import matplotlib.pyplot as plt

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
links = ["https://www.tradingview.com/symbols/TVC-US01Y/", "https://www.tradingview.com/symbols/TVC-US02Y/",
         "https://www.tradingview.com/symbols/TVC-US03Y/", "https://www.tradingview.com/symbols/TVC-US05Y/",
         "https://www.tradingview.com/symbols/TVC-US07Y/", "https://www.tradingview.com/symbols/TVC-US10Y/",
         "https://www.tradingview.com/symbols/TVC-US20Y/", "https://www.tradingview.com/symbols/TVC-US30Y/"]
data = []
for i in links:
    driver.get(i)
    time.sleep(3)
    price_element = driver.find_element(By.CLASS_NAME, "quotesRow-pAUXADuj")
    price = ''
    for i in price_element.text.split("\n")[0]:
        if i.isdigit() or i == ".":
            price += i
    data.append(float(price))
driver.close()
driver.quit()

plt.style.use('dark_background')

fig, ax = plt.subplots()

x = np.arange(len(data))

curve_degree = 4 # Degree of the polynomial curve

curve_coefficients = np.polyfit(x, data, curve_degree)
curve = np.poly1d(curve_coefficients)

curve_x = np.linspace(x[0], x[-1], 100)  # Generate more points for smoother curve
curve_y = curve(curve_x)

line_color = 'red'  # Set the desired line color
data_color = (0.4, 0.7, 1.0)

ax.plot(x, data, color=data_color, marker='o', linestyle='', label='Data', alpha=0.5)
ax.plot(curve_x, curve_y, color=line_color, linestyle='-', label='Curve', linewidth=3)
custom_labels = ['US01Y', 'US02Y', 'US03Y', 'US05Y', 'US07Y', 'US10Y', 'US20Y', 'US30Y']

ax.set_xlabel('Bonds by Maturity')
ax.set_xticks(x)  # Set x-axis ticks
ax.set_xticklabels(custom_labels)

ax.set_ylabel('Yield in %')
ax.set_title("Yield Curve")

ax.legend()
plt.savefig('graph.png', dpi=300)
plt.show()



# import time
# from requests_html import HTMLSession
#
# session = HTMLSession()
# session.headers[
#     "User-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
# session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
# session.headers["Accept-Language"] = "en-GB,en;q=0.9"
# session.headers["Connections"] = "keep-alive"
# session.headers["Upgrade-Insecure-Requests"] = "1"
# url = "https://www.tradingview.com/symbols/GOLD/"
# response = session.get(url)
# price = response.html.find()
# for i in price:
#     print(i.text)
