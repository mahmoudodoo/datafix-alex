import pandas as pd
import os
import requests

# Function to download an image from a given URL and save it to the specified folder
def download_image(url, folder):
    # Extract the image file name from the URL
    image_name = url.split("/")[-1]
    
    try:
        # Send an HTTP request to fetch the image
        response = requests.get(f"http://{url}", stream=True)
        response.raise_for_status()  # Check for HTTP errors

        # Save the image to the specified folder
        image_path = os.path.join(folder, image_name)
        with open(image_path, 'wb') as image_file:
            for chunk in response.iter_content(1024):
                image_file.write(chunk)
        print(f"Downloaded: {image_name}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_name}. Error: {e}")

# Function to extract the bucket name from the image URL
def get_bucket_name(url):
    # Assuming the bucket name is the first part of the URL, e.g., 's3.amazonaws.com'
    return url.split("/")[0]

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
        # Loop through the 'Flower Image' column and download each image
        for index, url in df['Flower Image'].items():  # Changed iteritems() to items()
            if isinstance(url, str):
                # Fix the URL if it starts with '//'
                if url.startswith('//'):
                    url = url[2:]
                
                # Get the bucket name from the URL
                bucket_name = get_bucket_name(url)

                # Create a directory for the bucket if it doesn't exist
                if not os.path.exists(bucket_name):
                    os.makedirs(bucket_name)

                # Download the image and save it to the corresponding bucket folder
                download_image(url, bucket_name)
