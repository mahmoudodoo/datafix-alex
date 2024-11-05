import pandas as pd
import os

# Get the CSV file name from the user after exporting from Numbers
file_name = input("Enter the exported CSV file name (including the extension): ")

# Check if the file exists in the current working directory
if not os.path.isfile(file_name):
    print(f"The file '{file_name}' does not exist in the current directory.")
else:
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_name)

    # Remove duplicates
    df_cleaned = df.drop_duplicates()

    # Save the cleaned data to a new CSV file
    new_file_name = f"cleaned_{file_name}"
    df_cleaned.to_csv(new_file_name, index=False)

    print(f"Duplicates removed. The cleaned file has been saved as '{new_file_name}'.")
