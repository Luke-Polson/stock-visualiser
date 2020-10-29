import tkinter as tk
import numpy as np


class InfoWindow(tk.Tk):
    def __init__(self, info, prices):

        self.info = info
        self.prices = prices

        tk.Tk.__init__(self)

        self.title(info['symbol'] + " Info")
        self.configure(padx=10, pady=10)

        self.populate_window()

        self.mainloop()

    def populate_window(self):

        closing_prices = self.prices
        try:
            avg_volume = tk.Label(self, text="Average Volume: {:,}".format(self.info['averageVolume']))
            avg_volume.pack(side=tk.BOTTOM)
        except (KeyError, TypeError):
            pass

        try:
            eps = tk.Label(self, text="EPS (TTM): {:.2f}".format(self.info['trailingEps']))
            eps.pack(side=tk.BOTTOM)
        except (KeyError, TypeError):
            pass

        try:
            pe_ratio = tk.Label(self, text="P/E Ratio (TTM): {:.2f}".format(self.info['trailingPE']))
            pe_ratio.pack(side=tk.BOTTOM)

        except KeyError:
            # pass if the ticker has no p/e ratio listed
            pass

        try:
            market_cap = tk.Label(self, text="Market Cap: ${:,}".format(self.info['marketCap']))
            market_cap.pack(side=tk.BOTTOM)

            shares_outstanding = tk.Label(self,text="Outstanding Shares: {:,}".format(self.info['sharesOutstanding']))
            shares_outstanding.pack(side=tk.BOTTOM)

        except (KeyError, TypeError):
            # if ticker represents an index, don't include marketCap or sharesOutstanding
            pass

        # calculate standard deviation for the stock price over last year
        sigma = np.std([price for price in closing_prices[-1000:]])
        sigma_percentage = np.std([100.0 * a1 / a2 - 100 for a1, a2 in zip(closing_prices[1:], closing_prices)])

        volatility_label = tk.Label(self, text="Volatility: ${:,.2f} ({:.2f}%)"
                            .format(sigma, sigma_percentage), padx=10)

        volatility_label.pack(side=tk.BOTTOM)
