import pandas as pd

def get_country_histogram(data, doc_id):
    """Get a histogram of views by country for a specific document."""
    filtered_data = data[data['document_uuid'] == doc_id]
    return filtered_data['country'].value_counts()

def get_browser_histogram(data):
    """Get a histogram of views by browser."""
    return data['browser'].value_counts()
