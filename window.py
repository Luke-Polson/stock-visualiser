import tkinter as tk
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window:

    def __init__(self):

        # initialise root window
        self.root = tk.Tk()
        self.root.withdraw()

        self.button1 = None
        self.ticker_entry = None
        self.ticker_label = None

        # welcome window asks for a ticker as input
        self.welcome_window = tk.Toplevel(self.root)
        self.welcome_window.title("Please enter a valid ticker")

        # main window to display stock info
        self.main_window = tk.Toplevel(self.root)
        self.main_window.title("Stock Visualiser")

        self.populate_welcome()

        self.main_window.withdraw()

        self.root.mainloop()

    def populate_welcome(self):

        self.ticker_label = tk.Label(self.welcome_window, text="Enter a stock ticker, eg 'AAPL'",
                                     font=('', 20), padx=10, pady=10)

        self.ticker_label.grid(row=0, column=0)

        self.button1 = tk.Button(self.welcome_window, text='Go', width=20, pady=7, command=self.goto_main)
        self.ticker_entry = tk.Entry(self.welcome_window, textvariable=tk.StringVar)

        self.button1.grid(row=2, column=0, pady=10)
        self.ticker_entry.grid(row=1, column=0, pady=10)

    def goto_main(self):

        entered_ticker = self.ticker_entry.get()

        self.populate_main(entered_ticker)

        self.welcome_window.withdraw()
        self.main_window.deiconify()

    def populate_main(self, ticker):

        tick = yf.Ticker(ticker)

        hist = tick.history(period='1y')
        info = tick.info

        opening_prices = hist['Open']
        closing_prices = hist['Close']

        exit_button = tk.Button(self.main_window, text="Exit", command=self.exit, padx=5, pady=5)
        exit_button.pack(side=tk.TOP, pady=10)

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        chart_type = FigureCanvasTkAgg(fig, self.main_window)
        chart_type.get_tk_widget().pack(side=tk.TOP)

        change_stock = tk.Button(self.main_window, text="Change", command=self.change_stock, pady=5, padx=5)
        change_stock.pack(pady=10, padx=10, side=tk.BOTTOM)

        # plot the closing prices for the past year
        closing_prices.plot(title="Stock Price: {} ({})".format(info['longName'], ticker), ax=ax)

        share_label = tk.Label(self.main_window, text="Market Cap: ${:,} | "
                                                      "Outstanding Shares: {:,}"
                               .format(info['marketCap'], info['sharesOutstanding']))

        share_label.pack(side=tk.BOTTOM)

        # calculate standard deviation for the stock price over last year
        sigma = np.std([price for price in opening_prices[-1000:]])
        sigma_percentage = np.std([100.0 * a1 / a2 - 100 for a1, a2 in zip(opening_prices[1:], opening_prices)])

        volatility_label = tk.Label(self.main_window, text="Volatility: ${:,.3f} ({:.2f}%)"
                                    .format(sigma, sigma_percentage), padx=10)

        volatility_label.pack(side=tk.BOTTOM)

        # closing price from the day before, and closing price from the current day
        prices = tk.Label(self.main_window, text="Opening: ${:,.3f} | "
                                                 "Closing: ${:,.3f}"
                          .format(opening_prices[-1], closing_prices[-1]))

        prices.pack(side=tk.BOTTOM)

    def change_stock(self):

        self.root.destroy()

        self.__init__()

    def exit(self):

        self.root.destroy()



