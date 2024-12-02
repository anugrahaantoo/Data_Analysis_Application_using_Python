# data_analysis.py
import json
import pandas as pd
import re
from graphviz import Digraph

# Function to load data from a JSON file into a Pandas DataFrame
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
        df = pd.DataFrame(data)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
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

# Function to generate the "Also Likes" list
def also_likes(df, doc_uuid):
    readers = df[df['subject_doc_id'] == doc_uuid]['visitor_uuid'].unique()
    if not readers.size:
        return []
    all_docs = []
    for reader in readers:
        all_docs.extend(df[df['visitor_uuid'] == reader]['subject_doc_id'].unique())
    doc_counts = pd.Series(all_docs).value_counts()
    if doc_uuid in doc_counts.index:
        doc_counts = doc_counts.drop(doc_uuid)
    return doc_counts.head(10).index.tolist()

# Function to generate the "Also Likes" graph
def generate_also_likes_graph(df, doc_uuid):
    readers = df[df['subject_doc_id'] == doc_uuid]['visitor_uuid'].unique()
    if not readers.size:
        return None
    
    all_relationships = []
    for reader in readers:
        related_docs = df[df['visitor_uuid'] == reader]['subject_doc_id'].unique()
        for doc in related_docs:
            all_relationships.append((reader[-4:], doc[-4:]))
    
    graph = Digraph(format='pdf')
    graph.attr(rankdir='TB', size='8,5')
    graph.node(doc_uuid[-4:], label=f"{doc_uuid[-4:]}", style="filled", color="green")
    
    for reader in readers:
        graph.node(reader[-4:], label=f"{reader[-4:]}", style="filled", color="green")
    
    for reader, doc in all_relationships:
        graph.node(doc, label=doc)
        graph.edge(reader, doc)

    output_file = "also_likes_graph"
    graph.render(output_file, cleanup=True)
    return output_file
