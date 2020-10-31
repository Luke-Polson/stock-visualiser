import tkinter as tk
import matplotlib.pyplot as plt
import yfinance as yf
import info_window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)

        self.withdraw()

        self.button1 = None
        self.ticker_entry = None
        self.ticker_label = None
        self.prices = None
        self.info = None

        # welcome window asks for a ticker as input
        self.welcome_window = tk.Toplevel(self, padx=30, background="black")
        self.welcome_window.title("Please enter a valid ticker")

        # main window to display stock info
        self.main_window = tk.Toplevel(self, background="black")
        self.main_window.title("Stock Visualiser")

        self.populate_welcome()

        self.main_window.withdraw()

        self.mainloop()

    def populate_welcome(self):

        self.ticker_label = tk.Label(self.welcome_window, text="Enter a Ticker", font=('', 20), padx=10, pady=10)
        self.ticker_label.configure(bg='black', fg='white')
        self.ticker_label.grid(row=0, column=0)

        self.button1 = tk.Button(self.welcome_window, text='Go', width=20, pady=7, command=self.goto_main)
        self.ticker_entry = tk.Entry(self.welcome_window, textvariable=tk.StringVar)
        self.ticker_entry.configure(bg='black', fg='white')

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

        fig = plt.Figure()
        fig.set_facecolor("black")

        ax = fig.add_subplot(111)
        ax.set_facecolor("black")

        #ax.spines['bottom'].set_color("white")
        #ax.spines['left'].set_color("white")

        ax.tick_params(axis='x', colors='white', which='both')
        ax.tick_params(axis='y', colors='white', which='both')

        ax.title.set_color('white')

        chart_type = FigureCanvasTkAgg(fig, self.main_window)
        chart_type.get_tk_widget().pack(side=tk.BOTTOM)

        open = self.prices[-2]
        close = self.prices[-1]

        try:
            # if ticker doesn't have a listed name, just use the stock ticker
            name = self.info['longName']
        except KeyError:
            name = ""

        if close > open:
            color = "green"
        else:
            color = "red"

        # plot the closing prices for the past year
        self.prices.plot(title="Stock Price: {} ({})".format(name, ticker), ax=ax, color=color)

        # closing price from the day before, and closing price from the current day
        prices = tk.Label(self.main_window, text="Open: ${:,.2f} | "
                                                 "Close: ${:,.2f} | "
                                                 "({:,.2f}%)".format(open, close, 100*(close-open) / open), bg="black")

        if open > close:
            prices.configure(fg="red")
        else:
            prices.configure(fg="green")

        prices.pack(side=tk.BOTTOM)

        exit_button = tk.Button(self.main_window, text="Exit", command=self.exit, padx=10, pady=5)
        exit_button.pack(pady=10, side=tk.LEFT)

        change_stock = tk.Button(self.main_window, text="Change", command=self.change_stock, pady=5, padx=5)
        change_stock.pack(pady=10, padx=10, side=tk.LEFT)

        info_button = tk.Button(self.main_window, text="Info", command=self.display_info, padx=5, pady=5)
        info_button.pack(pady=10, side=tk.LEFT)

    def change_stock(self):

        self.destroy()

        self.__init__()

    def display_info(self):

        info = info_window.InfoWindow(self.info, self.prices)

    def exit(self):

        self.destroy()



