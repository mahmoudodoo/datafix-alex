import pandas as pd
import os

# Function to update type_id in arrangements using the arrangement_type file
def update_type_id(arrangements_file, arrangement_type_file):
    if not os.path.isfile(arrangements_file):
        print(f"The file '{arrangements_file}' does not exist in the current directory.")
        return
    if not os.path.isfile(arrangement_type_file):
        print(f"The file '{arrangement_type_file}' does not exist in the current directory.")
        return

    # Load the CSV files into pandas DataFrames
    arrangements_df = pd.read_csv(arrangements_file)
    arrangement_type_df = pd.read_csv(arrangement_type_file)
    
    # Check if necessary columns exist
    if 'type_id' not in arrangements_df.columns:
        print("The column 'type_id' does not exist in the arrangements CSV file.")
        return
    if 'id' not in arrangement_type_df.columns or 'Name' not in arrangement_type_df.columns:
        print("The required columns 'id' and 'Name' do not exist in the arrangement_type CSV file.")
        return

    # Create a dictionary mapping Name to id from the arrangement_type DataFrame
    type_name_to_id = pd.Series(arrangement_type_df.id.values, index=arrangement_type_df.Name).to_dict()

    # Update the type_id column in the arrangements DataFrame
    arrangements_df['type_id'] = arrangements_df['type_id'].map(type_name_to_id)

    # Save the updated DataFrame to a new CSV file
    output_file = f"updated_{arrangements_file}"
    arrangements_df.to_csv(output_file, index=False)
    print(f"Updated arrangements saved to '{output_file}'")

# Main function
if __name__ == "__main__":
    # Get the CSV file names from the user
    arrangements_file = input("Enter the arrangements CSV file name (including the extension): ")
    arrangement_type_file = input("Enter the arrangement_type CSV file name (including the extension): ")
    
    # Process the files to update type_id
    update_type_id(arrangements_file, arrangement_type_file)
