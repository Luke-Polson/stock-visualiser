import tkinter as tk
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import info_window

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window:

    def __init__(self):

        # initialise root window
        self.root = tk.Tk()
        self.root.withdraw()

        self.button1 = None
        self.ticker_entry = None
        self.ticker_label = None
        self.prices = None
        self.info = None

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

        self.ticker_label = tk.Label(self.welcome_window, text="Enter a Stock Ticker",
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
        self.info = tick.info

        self.prices = hist['Close']

        info_button = tk.Button(self.main_window, text="Info", command=self.display_info, padx=5, pady=5)
        info_button.pack(pady=5, side=tk.BOTTOM)

        exit_button = tk.Button(self.main_window, text="Exit", command=self.exit, padx=5, pady=5)
        exit_button.pack(pady=5, side=tk.TOP)

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        chart_type = FigureCanvasTkAgg(fig, self.main_window)
        chart_type.get_tk_widget().pack(side=tk.TOP)

        change_stock = tk.Button(self.main_window, text="Change", command=self.change_stock, pady=5, padx=5)
        change_stock.pack(pady=10, padx=10, side=tk.BOTTOM)

        # plot the closing prices for the past year

        try:
            # if ticker doesn't have a listed name, just use the stock ticker
            name = self.info['longName']
        except KeyError:
            name = ""

        self.prices.plot(title="Stock Price: {} ({})".format(name, ticker), ax=ax)

        open = self.prices[-2]
        close = self.prices[-1]

        # closing price from the day before, and closing price from the current day
        prices = tk.Label(self.main_window, text="Opening: ${:,.2f} | "
                                                 "Closing: ${:,.2f} | "
                                                 "({:,.2f}%)"
                                    .format(open, close, 100 * (close-open) / open))

        if open > close:
            prices.configure(fg="red")
        else:
            prices.configure(fg="green")

        prices.pack(side=tk.BOTTOM)

    def change_stock(self):

        self.root.destroy()

        self.__init__()

    def display_info(self):
        info = info_window.InfoWindow(self.info, self.prices)

    def exit(self):

        self.root.destroy()



