import json
import pandas as pd
import re
import dask.dataframe as dd
import gzip
from tkinter import messagebox

# Function to load data from a JSON file into a Pandas DataFrame
def load_data(file_path):
    try:
        # Check if the file is compressed
        if file_path.endswith('.gz'):
            with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                data = (json.loads(line) for line in file)
                df = pd.DataFrame(data)  # Convert generator to DataFrame
        else:
            dask_df = dd.read_json(file_path, lines=True)
            df = dask_df.compute()  # Convert Dask DataFrame to Pandas DataFrame
        return df

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        return None


# Extract main browser name using regex
def extract_browser_name(useragent):
    patterns = [
        (r"Chrome\/[\d\.]+", "Chrome"),
        (r"Firefox\/[\d\.]+", "Firefox"),
        (r"Safari\/[\d\.]+", "Safari"),
        (r"Edge\/[\d\.]+", "Edge"),
        (r"MSIE [\d\.]+", "Internet Explorer"),
        (r"Trident\/[\d\.]+", "Internet Explorer"),
        (r"Opera\/[\d\.]+", "Opera"),
        (r"Mozilla\/[\d\.]+", "Mozilla"),
    ]
    for pattern, browser_name in patterns:
        if re.search(pattern, useragent, re.IGNORECASE):
            return browser_name
    return "Unknown"

#extract browser verbose info 
def extract_detailed_browser_name(useragent):
    browser_name = extract_browser_name(useragent)
    # Extract OS details within parentheses
    os_match = re.search(r"\(([^)]+)\)", useragent)
    os_info = os_match.group(1) if os_match else "Unknown OS"
    return f"{browser_name} ({os_info})"


