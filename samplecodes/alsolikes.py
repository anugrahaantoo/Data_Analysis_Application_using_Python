import pandas as pd

def get_readers_of_document(data, doc_uuid):
    """
    Returns all visitor UUIDs who have read the given document.
    :param data: DataFrame containing 'subject_doc_id' and 'visitor_uuid'.
    :param doc_uuid: Document UUID for which readers are to be retrieved.
    :return: List of visitor UUIDs.
    """
    return data[data['subject_doc_id'] == doc_uuid]['visitor_uuid'].unique().tolist()

def get_documents_read_by_visitor(data, visitor_uuid):
    """
    Returns all document UUIDs read by a given visitor.
    :param data: DataFrame containing 'subject_doc_id' and 'visitor_uuid'.
    :param visitor_uuid: Visitor UUID for which documents are to be retrieved.
    :return: List of document UUIDs.
    """
    return data[data['visitor_uuid'] == visitor_uuid]['subject_doc_id'].unique().tolist()

def also_likes(data, doc_uuid, sorting_function, visitor_uuid=None):
    """
    Generate an 'also likes' list for the given document UUID.
    :param data: DataFrame containing 'subject_doc_id' and 'visitor_uuid'.
    :param doc_uuid: Document UUID to find 'also likes' for.
    :param sorting_function: Function to sort the results.
    :param visitor_uuid: Optional visitor UUID to filter for specific visitor data.
    :return: Sorted list of top 10 document UUIDs.
    """
    # Get readers of the given document
    readers = get_readers_of_document(data, doc_uuid)

    # Optionally filter readers for a specific visitor
    if visitor_uuid:
        readers = [visitor_uuid] if visitor_uuid in readers else []

    # Get documents liked by these readers
    liked_docs = data[data['visitor_uuid'].isin(readers)]['subject_doc_id']

    # Exclude the original document from the list
    liked_docs = liked_docs[liked_docs != doc_uuid]

    # Aggregate counts and apply sorting function
    doc_counts = liked_docs.value_counts()
    sorted_docs = sorting_function(doc_counts)

    # Return the top 10 document UUIDs
    return sorted_docs.head(10).index.tolist()

def sort_by_readers(doc_counts):
    """
    Sort documents by the number of readers.
    :param doc_counts: Pandas Series with document UUIDs as index and counts as values.
    :return: Sorted Series.
    """
    return doc_counts.sort_values(ascending=False)

# Example Usage
if __name__ == "__main__":
    # Example DataFrame
    data = pd.DataFrame({
        'subject_doc_id': ['doc1', 'doc2', 'doc1', 'doc3', 'doc2', 'doc4', 'doc3', 'doc5'],
        'visitor_uuid': ['reader1', 'reader1', 'reader2', 'reader2', 'reader3', 'reader3', 'reader4', 'reader4']
    })

    # Input document UUID
    doc_uuid = 'doc1'

    # Generate the "also likes" list
    also_likes_list = also_likes(data, doc_uuid)
    print("Top 10 'Also Liked' documents:", also_likes_list)
