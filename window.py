import tkinter as tk
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Window:

    def __init__(self):

        root = tk.Tk()
        root.withdraw()

        self.button1 = None
        self.ticker_entry = None
        self.ticker_label = None

        self.welcome_window = tk.Toplevel(root)
        self.welcome_window.title("Please enter a valid ticker")

        self.main_window = tk.Toplevel(root)
        self.main_window.title("Stock Visualiser")

        self.populate_welcome()

        self.main_window.withdraw()

        root.mainloop()

    def populate_welcome(self):

        self.ticker_label = tk.Label(self.welcome_window,
                                     text="Enter a stock ticker, eg 'AAPL'",
                                     font=('',20),
                                     padx=10,
                                     pady=10)

        self.ticker_label.grid(row=0,column=0)

        self.button1 = tk.Button(self.welcome_window, text='Go', width=20, command=self.goto_main)
        self.ticker_entry = tk.Entry(self.welcome_window, textvariable=tk.StringVar)

        self.button1.grid(row=2,column=0)
        self.ticker_entry.grid(row=1, column=0)

    def goto_main(self):

        # TODO: embed plot within main window
        # TODO: calculate info including volatility, percentage increases, etc

        entered_ticker = self.ticker_entry.get()

        data = yf.download(entered_ticker)

        self.populate_main(data, entered_ticker)

        self.welcome_window.destroy()
        self.main_window.deiconify()

    def populate_main(self, data, ticker):

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        chart_type = FigureCanvasTkAgg(fig, self.main_window)
        chart_type.get_tk_widget().pack()

        data['Adj Close'].plot(title="Stock Price: " + ticker, ax=ax)

        # calculate standard deviation for the stock price over last 1000 days
        sigma = np.std([price for price in data['Adj Close'][-1000:]])

        self.volatility_label = tk.Label(self.main_window, text="Volatility: ${:.3f}".format(sigma), padx=10)
        self.volatility_label.pack(side=tk.LEFT)






