import pandas as pd
import os

# Function to identify and add missing types to arrangement_type.csv
def add_missing_types(arrangements_file, arrangement_type_file):
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

    # Get the unique type names from the arrangements.csv (currently stored in 'type_id')
    arrangement_type_names_in_arrangements = arrangements_df['type_id'].dropna().unique()

    # Get the existing type names from arrangement_type.csv
    existing_type_names = arrangement_type_df['Name'].dropna().unique()

    # Identify missing type names by comparing both sets
    missing_type_names = set(arrangement_type_names_in_arrangements) - set(existing_type_names)

    # Remove any non-string types from the missing types (in case of floats or other invalid values)
    missing_type_names = {name for name in missing_type_names if isinstance(name, str)}

    # Create new DataFrame for missing types
    if missing_type_names:
        print(f"Found {len(missing_type_names)} missing types. Adding them to arrangement_type.csv...")

        # Create new DataFrame with missing types and assign new IDs
        new_types_df = pd.DataFrame({
            'id': range(arrangement_type_df['id'].max() + 1, arrangement_type_df['id'].max() + 1 + len(missing_type_names)),
            'Name': list(missing_type_names),
            'Creation Date': pd.Timestamp.now(),  # You can set this to any desired value
            'Modified Date': pd.Timestamp.now(),  # You can set this to any desired value
            'Slug': [name.lower().replace(' ', '-') for name in missing_type_names],  # Generate slugs
            'Creator': ['system'] * len(missing_type_names)  # Example value, adjust as needed
        })

        # Append the missing types to the existing arrangement_type DataFrame
        updated_arrangement_type_df = pd.concat([arrangement_type_df, new_types_df], ignore_index=True)

        # Save the updated arrangement_type DataFrame to a new CSV file
        updated_arrangement_type_file = f"updated_{arrangement_type_file}"
        updated_arrangement_type_df.to_csv(updated_arrangement_type_file, index=False)
        print(f"Missing types added and saved to '{updated_arrangement_type_file}'")
    else:
        print("No missing types found. The arrangement_type.csv file is up to date.")

# Main function
if __name__ == "__main__":
    # Get the CSV file names from the user
    arrangements_file = input("Enter the arrangements CSV file name (including the extension): ")
    arrangement_type_file = input("Enter the arrangement_type CSV file name (including the extension): ")

    # Add missing types to the arrangement_type file
    add_missing_types(arrangements_file, arrangement_type_file)
