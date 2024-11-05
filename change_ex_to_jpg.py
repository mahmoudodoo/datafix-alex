import pandas as pd
import os

# Function to update image URLs by changing extension to .jpg
def update_image_extension(image_url):
    if pd.isna(image_url):
        return image_url  # If the URL is NaN, return it unchanged

    # Check if the URL has an extension and change it to .jpg
    if isinstance(image_url, str):
        # Split the URL by '.' to isolate the extension
        parts = image_url.rsplit('.', 1)  # Split into [url, extension] at the last '.'
        if len(parts) > 1:
            # Replace the extension with .jpg
            return parts[0] + '.jpg'
    return image_url  # Return unchanged if no extension is found

# Function to process the CSV and update image extensions
def process_csv(file_name):
    if not os.path.isfile(file_name):
        print(f"The file '{file_name}' does not exist in the current directory.")
        return
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_name)

    # Check if the 'Image' column exists
    if 'Image' not in df.columns:
        print("The column 'Image' does not exist in the CSV file.")
        return
    
    # Loop through the 'Image' column and update each URL extension
    df['Image'] = df['Image'].apply(update_image_extension)

    # Save the updated DataFrame to a new CSV file
    output_file = f"updated_{file_name}"
    df.to_csv(output_file, index=False)
    print(f"Updated image extensions saved to '{output_file}'")

# Main function
if __name__ == "__main__":
    # Get the CSV file name from the user
    file_name = input("Enter the CSV file name (including the extension): ")
    
    # Process the CSV to update the image extensions
    process_csv(file_name)
