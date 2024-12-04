import pandas as pd

def get_readers_of_document(data, doc_uuid):
    """
    Returns all visitor UUIDs who have read the given document.
    :param data: DataFrame containing 'subject_doc_id' and 'visitor_uuid'.
    :param doc_uuid: Document UUID for which readers are to be retrieved.
    :return: List of visitor UUIDs.
    """
    readers = data[data['subject_doc_id'] == doc_uuid]['visitor_uuid'].unique().tolist()
    print(f"Readers of document {doc_uuid}: {readers}")
    return readers

def get_documents_read_by_visitor(data, visitor_uuid):
    """
    Returns all document UUIDs read by a given visitor.
    :param data: DataFrame containing 'subject_doc_id' and 'visitor_uuid'.
    :param visitor_uuid: Visitor UUID for which documents are to be retrieved.
    :return: List of document UUIDs.
    """
    docs = data[data['visitor_uuid'] == visitor_uuid]['subject_doc_id'].unique().tolist()
    print(f"Documents read by visitor {visitor_uuid}: {docs}")
    return docs

def also_likes(data, doc_uuid, sorting_function, visitor_uuid=None):
    """
    Generate an 'also likes' list for the given document UUID.
    :param data: DataFrame containing 'subject_doc_id' and 'visitor_uuid'.
    :param doc_uuid: Document UUID to find 'also likes' for.
    :param sorting_function: Function to sort the results.
    :param visitor_uuid: Optional visitor UUID to filter for specific visitor data.
    :return: Sorted list of top 10 document UUIDs.
    """
    print(f"\nAnalyzing document: {doc_uuid}")

    # Get readers of the given document
    readers = get_readers_of_document(data, doc_uuid)
    if not readers:
        print(f"No readers found for document {doc_uuid}.")
        return []

    # Optionally filter readers for a specific visitor
    if visitor_uuid:
        readers = [visitor_uuid] if visitor_uuid in readers else []
        print(f"Filtered readers for visitor {visitor_uuid}: {readers}")
        if not readers:
            print(f"No matching readers for visitor {visitor_uuid}.")
            return []

    # Get documents liked by these readers
    liked_docs = data[data['visitor_uuid'].isin(readers)]['subject_doc_id']
    print(f"Documents read by readers of {doc_uuid}: {liked_docs.tolist()}")

    # Exclude the original document from the list
    liked_docs = liked_docs[liked_docs != doc_uuid]
    print(f"Documents read by readers (excluding {doc_uuid}): {liked_docs.tolist()}")

    # Aggregate counts and apply sorting function
    doc_counts = liked_docs.value_counts()
    print(f"Document counts:\n{doc_counts}")

    sorted_docs = sorting_function(doc_counts)
    print(f"Sorted documents:\n{sorted_docs}")

    # Return the top 10 document UUIDs
    top_docs = sorted_docs.head(10).index.tolist()
    print(f"Top 10 'Also Liked' documents: {top_docs}")
    return top_docs

def sort_by_readers(doc_counts):
    """
    Sort documents by the number of readers.
    :param doc_counts: Pandas Series with document UUIDs as index and counts as values.
    :return: Sorted Series.
    """
    return doc_counts.sort_values(ascending=False)

if __name__ == "__main__":
    # Load the JSON file into a DataFrame
    file_path = r'C:\Users\Anmole\Downloads\sample_tiny.json'
    with open(file_path, 'r') as file:
        data = pd.read_json(file, lines=True)

    # Filter the required columns
    data = data[['subject_doc_id', 'visitor_uuid']]

    # Input document UUID
    doc_uuid = '100713205147-2ee05a98f1794324952eea5ca678c026'  # Replace with the target document ID

    # Generate the "also likes" list
    also_likes_list = also_likes(data, doc_uuid, sort_by_readers)
    print("\nFinal Output:")
    print("Top 10 'Also Liked' documents:", also_likes_list)
