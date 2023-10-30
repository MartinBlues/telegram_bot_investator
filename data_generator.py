import random
from datetime import datetime, timedelta
import pandas as pd

def generate_random_data():
    start_date = datetime(2023, 9, 27)
    end_date = datetime(2023, 10, 27)
    date_range = pd.date_range(start=start_date, end=end_date)

    data = {'Date': date_range, 'Buy Price': [random.uniform(150, 180) for _ in range(len(date_range))]}

    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False)

if __name__ == "__main__":
    generate_random_data()
