import pandas as pd
import os
import glob
from datetime import datetime

# Get current date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")

# Set the directory where your CSV files are stored
csv_directory = '/Users/timursalakhetdinov/Documents/Python_projects/Car_parsers/Auto_parsers/Bid_USA'  # Replace with the path to your CSV files
combined_csv_filename = f'bid_offers_{current_date}.csv'  # The filename for the combined CSV

# Change the working directory to the directory with CSVs
os.chdir(csv_directory)

# Use glob to match the pattern 'americanmotors_*.csv'
csv_files = glob.glob('bid_offers_*.csv')

# Initialize an empty list to store DataFrames
df_list = []

# Loop over the list of csv files
for file in csv_files:
    # Read the csv file and append it to the list of DataFrames
    df_list.append(pd.read_csv(file))

# Concatenate all DataFrames in the list
combined_df = pd.concat(df_list, ignore_index=True)

# Save the concatenated DataFrame to a single csv file
combined_df.to_csv(combined_csv_filename, index=False)

print(f'All CSV files have been combined into {combined_csv_filename}')
