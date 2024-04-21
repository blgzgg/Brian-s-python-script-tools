import requests
import pygal
import webbrowser
import datetime
import platform
import unittest

def intradaily(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=60min&apikey=K7HLGROEFZW2C06M'

def daily(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=full&apikey=K7HLGROEFZW2C06M'

def weekly(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + symbol + '&outputsize=full&apikey=K7HLGROEFZW2C06M'

def monthly(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + symbol + '&outputsize=full&apikey=K7HLGROEFZW2C06M'

def validate_symbol(symbol):
    return symbol.isalpha() and 1 <= len(symbol) <= 7 and symbol.isupper()

def validate_chart_type(chart_type):
    return chart_type in ['1', '2']

def validate_time_series(series_type):
    return series_type in ['1', '2', '3', '4']

def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class TestProject3Inputs(unittest.TestCase):

    def test_symbol(self):
        self.assertTrue(validate_symbol("GOOGL"))
        self.assertTrue(validate_symbol("AAPL"))
        self.assertFalse(validate_symbol("12345"))
        self.assertFalse(validate_symbol(""))

    def test_chart_type(self):
        self.assertTrue(validate_chart_type("1"))
        self.assertTrue(validate_chart_type("2"))
        self.assertFalse(validate_chart_type("3"))
        self.assertFalse(validate_chart_type(""))
        self.assertFalse(validate_chart_type("A"))

    def test_time_series(self):
        self.assertTrue(validate_time_series("1"))
        self.assertTrue(validate_time_series("2"))
        self.assertTrue(validate_time_series("3"))
        self.assertTrue(validate_time_series("4"))
        self.assertFalse(validate_time_series("5"))
        self.assertFalse(validate_time_series(""))
        self.assertFalse(validate_time_series("A"))

    def test_date(self):
        self.assertTrue(validate_date("2024-04-20"))
        self.assertFalse(validate_date("2024/04/20"))
        self.assertFalse(validate_date("20-04-2024"))
        self.assertFalse(validate_date(""))

def main():       
    while True:
        # Title Screen
        print("---------------------")
        print("Stock Data Visualizer")
        print("---------------------\n")
        
        # Ask the user to enter the stock symbol
        while True:
            stock_symbol = input("Enter The Stock Symbol You Are Looking For (ex: GOOGL): ")
            if validate_symbol(stock_symbol):
                break
            else:
                print("Please enter a valid stock symbol.")

        # Chart Type Screen
        print("\n-----------")
        print("Chart Types")
        print("-----------")
        print("1. Bar")
        print("2. Line\n")
        
        # Ask the User to enter the chart type
        chart_type = 0
        while True:
            try:
                chart_type = input("Enter The Chart Type (1 or 2): ")
                if validate_chart_type(chart_type):
                    break
                else:
                    print("Please enter either 1 or 2.")
            except ValueError:
                print("Please enter a valid number (1 or 2).")

        # Time Series Screen
        print("\n--------------------------------------------------------")
        print("Select the Time Series of the Chart you want to Generate")
        print("--------------------------------------------------------")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly\n")

        # Ask the user to enter time series
        series_type = 0
        while True:
            try:
                series_type = input("Enter Time Series Option(1, 2, 3, or 4): ")
                if validate_time_series(series_type):
                    break
                else:
                    print("Please enter either 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a valid number (1, 2, 3, or 4).")

        # Ask the user to enter start date and end date
        start_y, start_m, start_d, end_y, end_m, end_d = "", "", "", "", "", ""
        while True:
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            if validate_date(start_date) and validate_date(end_date):
                start_y, start_m, start_d = start_date.split('-')
                end_y, end_m, end_d = end_date.split('-')
                if (start_y, start_m, start_d) > (end_y, end_m, end_d):
                    print("Start date cannot be later than end date. Please try again.")
                else:
                    break
            else:
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")

        data = {}
        series_format = ""
        
        if series_type == '1':
            url = intradaily(stock_symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Time Series (60min)"
        elif series_type == '2':
            url = daily(stock_symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Time Series (Daily)"
        elif series_type == '3':
            url = weekly(stock_symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Weekly Time Series"
        elif series_type == '4':
            url = monthly(stock_symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Monthly Time Series"
        
        # defining lists to store data once the dates are filtered and sorted
        data_in_range = []
        data_sorted = []

        # moves all data entries that fall within the date range provided by user
        for x in data[series_format]:
            year, month, day = x.split('-')    
            if int(start_y) <= int(year) and int(end_y) >= int(year) and int(start_m) <= int(month) and int(end_m) >= int(month) and int(start_d) <= int(day) and int(end_d) >= int(day):
                stock_open = data[series_format][x]['1. open']
                stock_high = data[series_format][x]['2. high']
                stock_low = data[series_format][x]['3. low']
                stock_close = data[series_format][x]['4. close']
                data_in_range.append([x, stock_open, stock_high, stock_low, stock_close])

        # by default stock data is in reverse (most recent date first, earliest date last), this function goes through and puts all the stock data in chronological order
        data_length = len(data_in_range)
        for x in range(data_length):
            data_sorted.append(data_in_range[data_length - x - 1])

        # defining lists for the graph values to be stored in
        dates = []
        open_price = []
        high_price = []
        low_price = []
        close_price = []

        # assigning values to the lists
        for x in data_sorted:
            dates.append(x[0])
            open_price.append(float(x[1]))
            high_price.append(float(x[2]))
            low_price.append(float(x[3]))
            close_price.append(float(x[4]))

        # making the graph
        if chart_type == '1':
            bar_chart = pygal.Bar()
            bar_chart.title = 'Stock Data for ' + stock_symbol + ': ' + start_date + ' to ' + end_date # graph title
            bar_chart.x_labels = map(str, dates) # x axis
            bar_chart.add('Open', open_price) # open line
            bar_chart.add('High', high_price) # high line
            bar_chart.add('Low', low_price) # low line
            bar_chart.add('Close', close_price) # close line
            bar_chart.render_to_file('chart.svg')
            print("bar chart made")
        elif chart_type == '2':
            line_chart = pygal.Line()
            line_chart.title = 'Stock Data for ' + stock_symbol + ': ' + start_date + ' to ' + end_date # graph title
            line_chart.x_labels = map(str, dates) # x axis
            line_chart.add('Open', open_price) # open line
            line_chart.add('High', high_price) # high line
            line_chart.add('Low', low_price) # low line
            line_chart.add('Close', close_price) # close line
            line_chart.render_to_file('chart.svg')
            print("line chart made")

        if platform.system() == "Windows": # if user is using Windows it will choose this
            browser = webbrowser.get('windows-default') # default windows browser
            browser.open('chart.svg') # opening file in browser
        elif platform.system() == "Darwin": # if user is using macOS it will choose this
            browser = webbrowser.get('macosx') # default macOS browser
            browser.open('chart.svg')
        else: # couldn't find one for a default linux, but I assume most Linux users use firefox lol
            browser = webbrowser.get('firefox') # firefox lol
            browser.open('chart.svg')

        continue_stock = input("Would you like to view more stock data? Press 'y' to continue or Press 'n' to exit: ")
        if continue_stock.lower() == 'y':
            pass
        elif continue_stock.lower() == 'n':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please enter 'y' to continue or 'n' to exit.")

if __name__ == "__main__":
    unittest.main()
    main()
