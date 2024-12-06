# data_analysis.py
import json
import pandas as pd
import re
import dask.dataframe as dd

from tkinter import messagebox

# Function to load data from a JSON file into a Pandas DataFrame
def load_data(file_path):
    try:
        # Check if the file is compressed (ends with .gz)
        if file_path.endswith('.gz'):
            # Use Dask for large compressed JSON files
            df = dd.read_json(file_path, compression='gzip')
        else:
            # Use Dask for large uncompressed JSON files
            df = dd.read_json(file_path)
        
        # Compute the Dask DataFrame into a Pandas DataFrame
        df = df.compute()  # Converts Dask dataframe to a Pandas DataFrame
        return df
        
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found at {file_path}")
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"JSON decoding error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the data: {e}")

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

def extract_detailed_browser_name(useragent):
    """
    Extracts the main browser name along with OS information from the user-agent string.
    """
    browser_name = extract_browser_name(useragent)
    # Extract OS details within parentheses
    os_match = re.search(r"\(([^)]+)\)", useragent)
    os_info = os_match.group(1) if os_match else "Unknown OS"
    return f"{browser_name} ({os_info})"


