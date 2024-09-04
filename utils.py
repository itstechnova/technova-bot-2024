import pandas as pd
import asyncio
from datetime import datetime

def load_csv_to_dict(file_path):
    df = pd.read_csv(file_path)
    data_dict = df.set_index("Email").to_dict(orient="index")
    return data_dict

def update_dict_to_csv(file_path, data_dict):
    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    # Write DataFrame to CSV
    df.to_csv(file_path, index_label='Email')

# Function to read CSV and parse the data
def read_events_csv(file_path):
    df = pd.read_csv(file_path)
    announcements = []

    for _, row in df.iterrows():
        # Assuming CSV columns: 'title', 'description', 'time'
        title = row['title']
        description = row['description']
        time_str = row['time']
        announcement_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        announcements.append((title, description, announcement_time))

    return sorted(announcements, key=lambda x: x[2])
