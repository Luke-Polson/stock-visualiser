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

        self.ticker_label.grid(row=0,column=0)

        self.button1 = tk.Button(self.welcome_window, text='Go', width=20, pady=7, command=self.goto_main)
        self.ticker_entry = tk.Entry(self.welcome_window, textvariable=tk.StringVar)

        self.button1.grid(row=2,column=0, pady=10)
        self.ticker_entry.grid(row=1, column=0, pady=10)

    def goto_main(self):

        entered_ticker = self.ticker_entry.get()

        data = yf.download(entered_ticker)

        self.populate_main(data, entered_ticker)

        self.welcome_window.withdraw()
        self.main_window.deiconify()

    def populate_main(self, data, ticker):

        change_stock = tk.Button(self.main_window, text="Change", command=self.change_stock)
        change_stock.pack()

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        chart_type = FigureCanvasTkAgg(fig, self.main_window)
        chart_type.get_tk_widget().pack()

        # plot the closing prices for the past year
        data['Adj Close'][-365:].plot(title="Stock Price: " + ticker, ax=ax)

        # closing price from the day before, and closing price from the current day
        opening = tk.Label(self.main_window, text="Opening: ${:.3f}".format(data['Adj Close'][-2]))
        closing = tk.Label(self.main_window, text="Closing: ${:.3f}".format(data['Adj Close'][-1]))

        opening.pack(side=tk.LEFT)
        closing.pack(side=tk.LEFT)

        # calculate standard deviation for the stock price over last 1000 days
        sigma = np.std([price for price in data['Adj Close'][-1000:]])

        volatility_label = tk.Label(self.main_window, text="Volatility: ${:.3f}".format(sigma), padx=10)
        volatility_label.pack(side=tk.LEFT)

    def change_stock(self):

        self.root.destroy()

        self.__init__()



