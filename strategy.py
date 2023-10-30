import pandas as pd

def calculate_profit(data):
    capital = 1000000
    parts = 15

    capital_per_part = capital / parts

    profitable_trades = 0
    losing_trades = 0
    total_profit_percentage = 0

    for index, row in data.iterrows():
        buy_price = row['Buy Price']
        sell_price = buy_price * 1.04

        for i in range(parts):
            entry_price = buy_price * (1 + (i+1) * 0.02)
            position_size = capital_per_part / entry_price

            if entry_price >= sell_price:
                profitable_trades += 1
                total_profit_percentage += (sell_price / buy_price - 1) * 100
            else:
                losing_trades += 1

    return {
        'profitable_trades': profitable_trades,
        'losing_trades': losing_trades,
        'total_profit_percentage': total_profit_percentage
    }

def load_data():
    data = pd.read_csv('data.csv')
    return data
