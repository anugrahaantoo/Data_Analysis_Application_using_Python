import json
import pandas as pd
import matplotlib.pyplot as plt
import re

# Function to load JSON data into a pandas DataFrame
def load_data(file_path):
    """Load data from a JSON file into a Pandas DataFrame."""
    try:
        # Reading the file into a list of dictionaries
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
        
        # Create DataFrame from list of dictionaries
        df = pd.DataFrame(data)
        
        # Print columns and sample of data for inspection
        print("Columns in DataFrame:", df.columns)
        print("Sample data:")
        print(df.head())
        
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

# Function to generate country histogram
def generate_country_histogram(df, doc_uuid):
    """Generate a histogram of views by country for a given document UUID."""
    try:
        # Filter data by subject_doc_id (document identifier in the dataset)
        filtered_data = df[df['subject_doc_id'] == doc_uuid]
        
        # Check if 'visitor_country' column exists and is not empty
        if 'visitor_country' in filtered_data.columns and not filtered_data.empty:
            country_counts = filtered_data['visitor_country'].value_counts()
            country_counts.plot(kind='bar', title="Views by Country")
            plt.xlabel("Country")
            plt.ylabel("Number of Views")
            plt.show()
        else:
            print("'visitor_country' column is missing in the dataset or no matching data found.")
    except KeyError as e:
        print(f"Key error: {e}. Check if 'subject_doc_id' or 'visitor_country' exists in the dataset")

# Function to generate continent histogram
def generate_continent_histogram(df, doc_uuid, continent_mapping):
    """Generate a histogram of views by continent for a given document UUID."""
    try:
        # Map countries to continents using ISO3166 country codes
        df['continent'] = df['visitor_country'].map(continent_mapping).fillna('Unknown')
        
        # Print the mapping to check for NaN values
        print("Data with continent mapping:")
        print(df[['visitor_country', 'continent']].head(10))  # Preview the mapping
        
        # Filter data by subject_doc_id (document identifier in the dataset)
        filtered_data = df[df['subject_doc_id'] == doc_uuid]
        
        # Check if 'continent' column exists and is not empty
        if 'continent' in filtered_data.columns and not filtered_data.empty:
            continent_counts = filtered_data['continent'].value_counts()
            print("Continent Counts:", continent_counts)  # Print the continent counts
            continent_counts.plot(kind='bar', title="Views by Continent")
            plt.xlabel("Continent")
            plt.ylabel("Number of Views")
            plt.show()
        else:
            print("'continent' column is missing in the dataset or no matching data found.")
    except KeyError as e:
        print(f"Key error: {e}. Check if 'subject_doc_id' or 'visitor_country' exists in the dataset.")

# ISO3166 two-letter country code to continent mapping
continent_mapping = {
    "US": "North America", "CA": "North America", "MX": "North America",
    "BR": "South America", "AR": "South America", "CL": "South America", "CO": "South America", "PE": "South America",
    "DE": "Europe", "FR": "Europe", "IT": "Europe", "ES": "Europe", "GB": "Europe", "RU": "Europe", 
    "PL": "Europe", "SE": "Europe", "NL": "Europe", "BE": "Europe", "AT": "Europe", "CH": "Europe",
    "IN": "Asia", "CN": "Asia", "JP": "Asia", "KR": "Asia", "SG": "Asia", "MY": "Asia", "ID": "Asia", 
    "TH": "Asia", "PH": "Asia", "VN": "Asia", "PK": "Asia", "BD": "Asia", "IR": "Asia", "IQ": "Asia", "SA": "Asia",
    "ZA": "Africa", "EG": "Africa", "NG": "Africa", "KE": "Africa", "GH": "Africa", "DZ": "Africa", 
    "MA": "Africa", "TZ": "Africa", "UG": "Africa", "SN": "Africa", "MW": "Africa", "ZM": "Africa", "MZ": "Africa",
    "AU": "Oceania", "NZ": "Oceania", "FJ": "Oceania", "PG": "Oceania", "WS": "Oceania", "VU": "Oceania",
    "TR": "Middle East", "AE": "Middle East", "IL": "Middle East", "KW": "Middle East", "QA": "Middle East",
    "SA": "Middle East", "JO": "Middle East", "LB": "Middle East", "OM": "Middle East", "BH": "Middle East",
    "LK": "Asia", "BD": "Asia", "MM": "Asia", "NP": "Asia", "LA": "Asia", "KH": "Asia"
}

# Task (a): Generate a histogram of all browser identifiers
def generate_browser_histogram(df):
    """Generate a histogram of views by full user agent string."""
    try:
        # Count occurrences of each visitor_useragent
        if 'visitor_useragent' in df.columns:
            useragent_counts = df['visitor_useragent'].value_counts()
            useragent_counts.plot(kind='bar', title="Views by Browser (Full User Agent)")
            plt.xlabel("User Agent")
            plt.ylabel("Number of Views")
            plt.show()
        else:
            print("'visitor_useragent' column is missing in the dataset")
    except KeyError as e:
        print(f"Key error: {e}. Check if 'visitor_useragent' exists in the dataset")

# Task (b): Extract the main browser name from the user agent string using regex
def extract_browser_name(useragent):
    """Extract the main browser name from the user agent string using regex."""
    # Regex pattern for common browser names
    patterns = [
        (r"Chrome\/[\d\.]+", "Chrome"),
        (r"Firefox\/[\d\.]+", "Firefox"),
        (r"Safari\/[\d\.]+", "Safari"),
        (r"Edge\/[\d\.]+", "Edge"),
        (r"MSIE [\d\.]+", "Internet Explorer"),
        (r"Trident\/[\d\.]+", "Internet Explorer"),  # For IE 11+
        (r"Opera\/[\d\.]+", "Opera"),
        (r"Mozilla\/[\d\.]+", "Mozilla"),  # Catch-all for others like Mozilla
    ]
    
    # Iterate over the patterns and match the browser name
    for pattern, browser_name in patterns:
        if re.search(pattern, useragent, re.IGNORECASE):
            return browser_name
    return "Unknown"  # Default if no browser is matched

def generate_main_browser_histogram(df):
    """Generate a histogram of views by main browser name."""
    try:
        if 'visitor_useragent' in df.columns:
            # Extract the main browser name for each user agent
            df['main_browser'] = df['visitor_useragent'].apply(extract_browser_name)
            
            # Count occurrences of each main browser
            browser_counts = df['main_browser'].value_counts()
            print("Main Browser Counts:", browser_counts)  # Print for inspection
            browser_counts.plot(kind='bar', title="Views by Main Browser")
            plt.xlabel("Browser")
            plt.ylabel("Number of Views")
            plt.show()
        else:
            print("'visitor_useragent' column is missing in the dataset")
    except KeyError as e:
        print(f"Key error: {e}. Check if 'visitor_useragent' exists in the dataset")

def analyze_top_readers(df):
    """Analyze and display the top 10 readers based on total reading time."""
    try:
        if 'visitor_uuid' in df.columns and 'event_readtime' in df.columns:
            # Group by visitor_uuid and sum the event_readtime
            reader_times = df.groupby('visitor_uuid')['event_readtime'].sum()

            # Sort the readers by total reading time in descending order
            top_readers = reader_times.nlargest(10)

            # Print the top 10 readers
            print("\nTop 10 Readers (Total Time Spent in Seconds):")
            print(top_readers)
        else:
            print("'visitor_uuid' or 'event_readtime' column is missing in the dataset.")
    except KeyError as e:
        print(f"Key error: {e}. Check if 'visitor_uuid' or 'event_readtime' exists in the dataset.")

# Main function to run the code
def main():
    # Load the data
    file_path = input("Enter the path to the JSON file: ")
    df = load_data(file_path)
    
    if df is not None:
        # Task (a): Generate and display the full user agent histogram
        print("Generating Full Browser Histogram...")
        generate_browser_histogram(df)

        # Task (b): Generate and display the main browser histogram
        print("Generating Main Browser Histogram...")
        generate_main_browser_histogram(df)

        # Task (c): Generate and display the country histogram
        doc_uuid = input("Enter Document UUID: ").strip()
        print("Generating Country Histogram...")
        generate_country_histogram(df, doc_uuid)

        # Task (d): Generate and display the continent histogram
        print("Generating Continent Histogram...")
        generate_continent_histogram(df, doc_uuid, continent_mapping)

        # Task (e): Analyze and display the top 10 readers
        print("\nAnalyzing Reader Profiles...")
        analyze_top_readers(df)

if __name__ == "__main__":
    main()
