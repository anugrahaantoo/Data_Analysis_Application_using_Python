import matplotlib.pyplot as plt
from data_processing import extract_browser_name, extract_detailed_browser_name

#method to display the country histogram
def country_histogram(df, doc_uuid):
    #select the data baed on the input document id
    selected_data = df[df['subject_doc_id'] == doc_uuid]
    #take the count of the country
    country_count = selected_data['visitor_country'].value_counts()
    plt.figure(figsize=(7, 4))  
    country_count.plot(kind='bar', title="Views by Country")
    plt.xlabel("Country")
    plt.ylabel("Number of Views")
    plt.tight_layout()  
    plt.show()

#method to display the continent histogram
def continent_histogram(df, doc_uuid, continent_mapping):
    #new column added to the dataframe by mapping to the continent mapping based on countries
    df['continent'] = df['visitor_country'].map(continent_mapping).fillna('Unknown')
    #select the data baed on the input document id
    selected_data = df[df['subject_doc_id'] == doc_uuid]
    #take the count of the contients
    continent_count = selected_data['continent'].value_counts()
    plt.figure(figsize=(7, 4)) 
    continent_count.plot(kind='bar', title="Views by Continent")
    plt.xlabel("Continent")
    plt.ylabel("Number of Views")
    plt.tight_layout() 
    plt.show()

#method to display the brower histogram with only the main name
def browser_histogram(df):
    #extract the browser name for the visitor_useragent and create a column main_browser
    df['main_browser'] = df['visitor_useragent'].apply(lambda x: extract_browser_name(x))
    #tsake the count of the browser
    browser_count = df['main_browser'].value_counts()
    plt.figure(figsize=(7, 4))  
    browser_count.plot(kind='bar', title="Views by Main Browser")
    plt.xlabel("Browser")
    plt.ylabel("Number of Views")
    plt.tight_layout()  
    plt.show()

#method to display the verbose browser details
def detailed_browser_histogram(df):
    # Extract detailed browser names
    df['detailed_browser'] = df['visitor_useragent'].apply(extract_detailed_browser_name)
    # take the count of the browsers
    browser_count = df['detailed_browser'].value_counts()
    browser_count.plot(kind='bar', figsize=(12, 6))
    plt.title('Histogram of Detailed Browser Names')
    plt.xlabel('Browser Name (with OS)')
    plt.ylabel('Number of Viewers')
    plt.show()

