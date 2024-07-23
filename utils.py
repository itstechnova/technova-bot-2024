import pandas as pd
def load_csv_to_dict(file_path):
    df = pd.read_csv(file_path)
    data_dict = df.set_index("Email").to_dict(orient="index")
    return data_dict

def update_dict_to_csv(file_path, data_dict):
    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    # Write DataFrame to CSV
    df.to_csv(file_path, index_label='Email')
