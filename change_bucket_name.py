import pandas as pd
import os

# Function to replace old bucket URLs with new bucket format for S3
def update_image_url(old_url, new_bucket):
    # Check if the URL is not NaN and is a valid string
    if pd.isna(old_url):
        return old_url  # Return as is if it's NaN (empty)

    if isinstance(old_url, str) and ("cdn.bubble.io" in old_url or "s3.amazonaws.com" in old_url):
        # Extract the file name and extension from the old URL
        parts = old_url.split('/')
        image_name_with_extension = parts[-1]  # Example: 'image.jpg'
        image_id = parts[-2]  # Example: 'f1682790343653x558813842294687360'

        # Create the new S3 path with the specified format
        new_url = f"https://s3.us-east-2.amazonaws.com/{new_bucket}/uploads/{image_id}.{image_name_with_extension.split('.')[-1]}"
        return new_url
    else:
        return old_url  # If it's not one of the recognized patterns, return it unchanged

# Function to process the CSV and update image URLs
def process_csv(file_name, new_bucket="wpro.ai"):
    if not os.path.isfile(file_name):
        print(f"The file '{file_name}' does not exist in the current directory.")
        return
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_name)

    # Check if the 'Image' column exists
    if 'Image' not in df.columns:
        print("The column 'Image' does not exist in the CSV file.")
        return
    
    # Loop through the 'Image' column and update each URL
    df['Image'] = df['Image'].apply(lambda url: update_image_url(url, new_bucket))

    # Save the updated DataFrame to a new CSV file
    output_file = f"updated_{file_name}"
    df.to_csv(output_file, index=False)
    print(f"Updated image URLs saved to '{output_file}'")

# Main function
if __name__ == "__main__":
    # Get the CSV file name from the user
    file_name = input("Enter the CSV file name (including the extension): ")
    
    # Process the CSV to update the image URLs
    process_csv(file_name, new_bucket="wpro.ai")
