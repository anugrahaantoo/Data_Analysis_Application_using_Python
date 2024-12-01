import matplotlib.pyplot as plt

def analyze_views_by_country(data, doc_id):
    """Visualize views by country for a specific document."""
    filtered_data = data[data['document_uuid'] == doc_id]
    country_counts = filtered_data['country'].value_counts()
    country_counts.plot(kind='bar')
    plt.title("Views by Country")
    plt.xlabel("Country")
    plt.ylabel("Number of Views")
    plt.show()

def analyze_views_by_continent(data, doc_id, continent_mapping):
    """Visualize views by continent for a specific document."""
    data['continent'] = data['country'].map(continent_mapping)
    filtered_data = data[data['document_uuid'] == doc_id]
    continent_counts = filtered_data['continent'].value_counts()
    continent_counts.plot(kind='bar')
    plt.title("Views by Continent")
    plt.xlabel("Continent")
    plt.ylabel("Number of Views")
    plt.show()
