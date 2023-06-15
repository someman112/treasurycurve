import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import interp1d
import numpy as np

plt.style.use('dark_background')
fig, ax = plt.subplots()


def animate(i):
    data = pd.read_csv('price_data.csv')
    y1 = data['price']

    # Perform polynomial curve fitting using least squares
    x_indices = range(len(y1))
    curve_degree = 24  # High degree of the polynomial curve

    curve_coefficients, residuals, _, _, _ = np.polyfit(x_indices, y1, curve_degree, full=True)
    curve = np.poly1d(curve_coefficients)

    curve_x = np.linspace(x_indices[0], x_indices[-1], 100)  # Generate more points for smoother curve
    curve_y = curve(curve_x)

    line_color = 'red'  # Set the desired line color
    data_color = (0.4, 0.7, 1.0)

    ax.cla()
    ax.plot(x_indices, y1, color=data_color, marker='o', linestyle='', label='Tick Data', alpha=0.15)
    ax.plot(curve_x, curve_y, color=line_color, linestyle='-', label='Price Aprox', linewidth=3)
    ax.legend()


ani = FuncAnimation(fig, animate, interval=2000, cache_frame_data=False)
plt.show()
