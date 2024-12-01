import json
import pandas as pd

def load_data(file_path):
    """Load data from a JSON file into a Pandas DataFrame."""
    try:
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                record = json.loads(line)
                
                # Check if 'document_uuid' exists in the record
                if 'document_uuid' not in record:
                    print("Warning: 'document_uuid' is missing in record:", record)
                    continue  # Skip this record if 'document_uuid' is missing
                
                data.append(record)
                
        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df
    
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
