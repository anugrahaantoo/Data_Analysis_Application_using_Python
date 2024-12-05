from graphviz import Digraph
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

def also_likes(data, doc_uuid, visitor_uuid=None):
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
    #sorted_docs = sorting_function(doc_counts)

    # Return the top 10 document UUIDs
    return doc_counts.head(10).index.tolist()


def generate_also_likes_graph(df, doc_uuid, visitor_uuid=None):
    """
    Generate an 'Also Likes' graph with ranks for readers and documents.
    Highlight the input document and optionally an input visitor.
    """
    # Get readers for the input document
    readers = df[df['subject_doc_id'] == doc_uuid]['visitor_uuid'].unique()
    if not readers.size:
        print("No readers found for the given document.")
        return None

    # Collect relationships for the graph
    all_relationships = []
    for reader in readers:
        related_docs = df[df['visitor_uuid'] == reader]['subject_doc_id'].unique()
        for doc in related_docs:
            all_relationships.append((reader[-4:], doc[-4:]))

    # Create the Graphviz Digraph
    graph = Digraph(format='pdf')
    graph.attr(ranksep='.75', ratio='compress', size='15,22', orientation='landscape', rotate='180')

    # Highlight the input document
    graph.node(doc_uuid[-4:], label=f"{doc_uuid[-4:]}", shape="circle", style="filled", color=".3 .9 .7")

    # Add reader nodes
    for reader in readers:
        if reader == visitor_uuid:  # Highlight the input visitor
            graph.node(reader[-4:], label=f"{reader[-4:]}", shape="box", style="filled", color=".3 .9 .7")
        else:
            graph.node(reader[-4:], label=f"{reader[-4:]}", shape="box")

    # Add document nodes and arrows
    for reader, doc in all_relationships:
        if doc != doc_uuid[-4:]:
            graph.node(doc, label=f"{doc}", shape="circle")
        graph.edge(reader, doc)

    # Set ranks for Readers and Documents
    with graph.subgraph() as readers_rank:
        readers_rank.attr(rank="same")
        readers_rank.node("Readers")
        for reader in readers:
            readers_rank.node(reader[-4:])

    with graph.subgraph() as documents_rank:
        documents_rank.attr(rank="same")
        documents_rank.node("Documents")
        for _, doc in all_relationships:
            documents_rank.node(doc)

    # Render the graph to both .ps and .pdf formats
    output_base_path = f"also_likes_{doc_uuid[-4:]}"
    ps_output_path = graph.render(output_base_path, format='ps')  # PostScript
    pdf_output_path = graph.render(output_base_path, format='pdf')  # PDF

    print(f"Graph generated as PostScript: {ps_output_path}")
    print(f"Graph generated as PDF: {pdf_output_path}")
    
