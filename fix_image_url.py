import pandas as pd
import os

# Function to fix the image URLs
def fix_image_url(url):
    # Remove the leading '//' if it exists
    if isinstance(url, str) and url.startswith('//'):
        return url[2:]  # Remove the first two characters (//)
    return url  # If no '//' found, return the URL as is

# Get the CSV file name from the user
file_name = input("Enter the CSV file name (including the extension): ")

# Check if the file exists in the current working directory
if not os.path.isfile(file_name):
    print(f"The file '{file_name}' does not exist in the current directory.")
else:
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_name)

    # Check if the 'Flower Image' column exists
    if 'Flower Image' not in df.columns:
        print("The column 'Flower Image' does not exist in the CSV file.")
    else:
        # Apply the fix_image_url function to the 'Flower Image' column
        df['Flower Image'] = df['Flower Image'].apply(fix_image_url)

        # Save the cleaned data back to a new CSV file
        new_file_name = f"fixed_{file_name}"
        df.to_csv(new_file_name, index=False)

        print(f"Image URLs in the 'Flower Image' column have been fixed and saved to '{new_file_name}'.")
