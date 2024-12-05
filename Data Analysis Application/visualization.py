import matplotlib.pyplot as plt
from data_analysis import extract_browser_name

def generate_country_histogram(df, doc_uuid):
    filtered_data = df[df['subject_doc_id'] == doc_uuid]
    country_counts = filtered_data['visitor_country'].value_counts()
    plt.figure(figsize=(7, 4))  # Set dimensions to 10x6 inches
    country_counts.plot(kind='bar', title="Views by Country")
    plt.xlabel("Country")
    plt.ylabel("Number of Views")
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()

def generate_continent_histogram(df, doc_uuid, continent_mapping):
    df['continent'] = df['visitor_country'].map(continent_mapping).fillna('Unknown')
    filtered_data = df[df['subject_doc_id'] == doc_uuid]
    continent_counts = filtered_data['continent'].value_counts()
    plt.figure(figsize=(7, 4))  # Set dimensions to 10x6 inches
    continent_counts.plot(kind='bar', title="Views by Continent")
    plt.xlabel("Continent")
    plt.ylabel("Number of Views")
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()

def generate_main_browser_histogram(df):
    df['main_browser'] = df['visitor_useragent'].apply(lambda x: extract_browser_name(x))
    browser_counts = df['main_browser'].value_counts()
    plt.figure(figsize=(7, 4))  # Set dimensions to 10x6 inches
    browser_counts.plot(kind='bar', title="Views by Main Browser")
    plt.xlabel("Browser")
    plt.ylabel("Number of Views")
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()
