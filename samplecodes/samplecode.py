import json
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph
import re

# Function to load JSON data into a pandas DataFrame
def load_data(file_path):
    """Load data from a JSON file into a Pandas DataFrame."""
    try:
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
        df = pd.DataFrame(data)
        print("Columns in DataFrame:", df.columns)
        print("Sample data:\n", df.head())
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

# Function to generate a histogram of views by country
def generate_country_histogram(df, doc_uuid):
    """Generate a histogram of views by country for a given document UUID."""
    try:
        if 'subject_doc_id' not in df.columns or 'visitor_country' not in df.columns:
            print("Missing required columns: 'subject_doc_id' or 'visitor_country'")
            return
        filtered_data = df[df['subject_doc_id'] == doc_uuid]
        if filtered_data.empty:
            print(f"No data found for Document UUID: {doc_uuid}")
            return
        country_counts = filtered_data['visitor_country'].value_counts()
        country_counts.plot(kind='bar', title="Views by Country")
        plt.xlabel("Country")
        plt.ylabel("Number of Views")
        plt.show()
    except Exception as e:
        print(f"Error generating country histogram: {e}")

# Function to generate a histogram of views by continent
def generate_continent_histogram(df, doc_uuid, continent_mapping):
    """Generate a histogram of views by continent for a given document UUID."""
    try:
        if 'visitor_country' not in df.columns:
            print("Missing 'visitor_country' column in dataset.")
            return
        df['continent'] = df['visitor_country'].map(continent_mapping).fillna('Unknown')
        filtered_data = df[df['subject_doc_id'] == doc_uuid]
        if filtered_data.empty:
            print(f"No data found for Document UUID: {doc_uuid}")
            return
        continent_counts = filtered_data['continent'].value_counts()
        continent_counts.plot(kind='bar', title="Views by Continent")
        plt.xlabel("Continent")
        plt.ylabel("Number of Views")
        plt.show()
    except Exception as e:
        print(f"Error generating continent histogram: {e}")

# Function to generate a histogram of views by main browser name
def generate_main_browser_histogram(df):
    """Generate a histogram of views by main browser name."""
    try:
        if 'visitor_useragent' not in df.columns:
            print("Missing 'visitor_useragent' column in dataset.")
            return
        df['main_browser'] = df['visitor_useragent'].apply(extract_browser_name)
        browser_counts = df['main_browser'].value_counts()
        browser_counts.plot(kind='bar', title="Views by Main Browser")
        plt.xlabel("Browser")
        plt.ylabel("Number of Views")
        plt.show()
    except Exception as e:
        print(f"Error generating main browser histogram: {e}")

# Extract main browser name using regex
def extract_browser_name(useragent):
    """Extract main browser name from user agent string."""
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

# Function to analyze and display the top 10 readers
def analyze_top_readers(df):
    """Analyze and display the top 10 readers based on total reading time."""
    try:
        if 'visitor_uuid' not in df.columns or 'event_readtime' not in df.columns:
            print("Missing required columns: 'visitor_uuid' or 'event_readtime'")
            return
        reader_times = df.groupby('visitor_uuid')['event_readtime'].sum()
        top_readers = reader_times.nlargest(10)
        print("\nTop 10 Readers (Total Time Spent in Seconds):")
        print(top_readers)
    except Exception as e:
        print(f"Error analyzing top readers: {e}")

# "Also Likes" functionality
def also_likes(df, doc_uuid):
    """Generate top 10 'also liked' documents for a given document UUID."""
    try:
        if 'subject_doc_id' not in df.columns or 'visitor_uuid' not in df.columns:
            print("Missing required columns: 'subject_doc_id' or 'visitor_uuid'")
            return
        readers = df[df['subject_doc_id'] == doc_uuid]['visitor_uuid'].unique()
        if not readers.size:
            print(f"No readers found for Document UUID: {doc_uuid}")
            return
        all_docs = []
        for reader in readers:
            all_docs.extend(df[df['visitor_uuid'] == reader]['subject_doc_id'].unique())
        doc_counts = pd.Series(all_docs).value_counts()
        if doc_uuid in doc_counts.index:
            doc_counts = doc_counts.drop(doc_uuid)
        print("\nTop 10 'Also Liked' Documents:")
        print(doc_counts.head(10))
    except Exception as e:
        print(f"Error generating 'Also Likes' recommendations: {e}")

def generate_also_likes_graph(df, doc_uuid):
    """Generate a graph of 'also likes' relationships for a given document UUID."""
    try:
        if 'subject_doc_id' not in df.columns or 'visitor_uuid' not in df.columns:
            print("Missing required columns: 'subject_doc_id' or 'visitor_uuid'")
            return
        
        # Filter readers of the input document
        readers = df[df['subject_doc_id'] == doc_uuid]['visitor_uuid'].unique()
        if not readers.size:
            print(f"No readers found for Document UUID: {doc_uuid}")
            return
        
        # Gather all related documents
        all_relationships = []
        for reader in readers:
            related_docs = df[df['visitor_uuid'] == reader]['subject_doc_id'].unique()
            for doc in related_docs:
                all_relationships.append((reader[-4:], doc[-4:]))
        
        # Create the graph
        graph = Digraph(format='pdf')
        graph.attr(rankdir='TB', size='8,5')
        
        # Highlight input document and readers
        graph.node(doc_uuid[-4:], label=f"{doc_uuid[-4:]}", style="filled", color="green")
        for reader in readers:
            graph.node(reader[-4:], label=f"{reader[-4:]}", style="filled", color="green")
        
        # Add relationships
        for reader, doc in all_relationships:
            graph.node(doc, label=doc)  # Document nodes
            graph.edge(reader, doc)  # Reader to document
        
        # Render the graph
        output_file = "also_likes_graph"
        graph.render(output_file, cleanup=True)
        print(f"Graph saved as {output_file}.pdf")
    except Exception as e:
        print(f"Error generating 'Also Likes' graph: {e}")

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

# Main function
def main():
    file_path = input("Enter the dataset file path: ")
    df = load_data(file_path)
    if df is not None:
        print("Generating Main Browser Histogram...")
        generate_main_browser_histogram(df)
        doc_uuid = input("Enter Document UUID: ").strip()
        print("Generating Country Histogram...")
        generate_country_histogram(df, doc_uuid)
        print("Generating Continent Histogram...")
        generate_continent_histogram(df, doc_uuid, continent_mapping)
        print("Analyzing Reader Profiles...")
        analyze_top_readers(df)
        print("Generating 'Also Likes' Recommendations...")
        also_likes(df, doc_uuid)
        print("Generating 'Also Likes' Graph...")
        generate_also_likes_graph(df, doc_uuid)

if __name__ == "__main__":
    main()
