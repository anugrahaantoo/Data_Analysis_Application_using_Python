from graphviz import Digraph
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# method returns the visitor ids for the given doc id if the event_type is read
def get_readers_of_document(data, doc_uuid):

    return data[(data['subject_doc_id'] == doc_uuid) & (data['event_type'] == 'read')]['visitor_uuid'].unique().tolist()

#method returns the list of documents for a visitor id if the event type is read
def get_documents_read_by_visitor(data, visitor_uuid):
  
    return data[(data['visitor_uuid'] == visitor_uuid) & (data['event_type'] == 'read')]['subject_doc_id'].unique().tolist()

#method to generate the also likes list
def also_likes(data, doc_uuid, visitor_uuid=None):
    # Get readers of the given document
    doc_readers = get_readers_of_document(data, doc_uuid)

    # add the user entered visitor id if not present in the list
    if visitor_uuid and visitor_uuid not in doc_readers:
        doc_readers.append(visitor_uuid)

    # Get documents liked by these readers
    liked_docs = []
    for reader in doc_readers:
        liked_docs.extend(get_documents_read_by_visitor(data, reader))

    # Exclude the original document from the list
    liked_docs = pd.Series(liked_docs)
    liked_docs = liked_docs[liked_docs != doc_uuid]

    # take the count and apply sorting function
    doc_counts = liked_docs.value_counts()
    sorted_docs = sorting_function(doc_counts)

    # Return the top 10 document UUIDs
    return sorted_docs.head(10).index.tolist()


#method that sorts the document counts in descending order
def sorting_function(doc_counts):

    return doc_counts.sort_values(ascending=False)

#method to generate the also likes graph
def also_likes_graph(data, doc_uuid, visitor_uuid=None):
   
    # Readers of the input document
    doc_readers = get_readers_of_document(data, doc_uuid)

    # Ensure visitor_uuid is added to doc_readers if provided
    if visitor_uuid and visitor_uuid not in doc_readers:
        doc_readers.append(visitor_uuid)

    # call also_likes function and get the list of documents
    related_docs = also_likes(data, doc_uuid)
    filtered_docs = []  # Will store documents read by input document readers
    shared_readers = {}  # Readers for each filtered document

    for related_doc in related_docs:
        # Readers of this "also liked" document
        related_readers = get_readers_of_document(data, related_doc)
        # Filter to keep only those who also read the input document
        common_readers = list(set(doc_readers) & set(related_readers))
        if common_readers:
            filtered_docs.append(related_doc)
            shared_readers[related_doc] = common_readers

    # Create a directed graph
    graph = Digraph(format='png')
    graph.attr(ranksep='1.0', size='15,10', ratio='compress')

    # Highlight the input document node
    graph.node(
        str(doc_uuid)[-4:], 
        label=f"{str(doc_uuid)[-4:]}", 
        shape="circle", 
        style="filled", 
        color="lightgreen"
    )

    # Add nodes for filtered "also liked" documents
    for related_doc in filtered_docs:
        graph.node(
            str(related_doc)[-4:], 
            label=f"{str(related_doc)[-4:]}", 
            shape="circle"
        )

    # Track added edges to avoid duplicates
    added_edges = set()

    # Add reader nodes and edges
    for related_doc, readers in shared_readers.items():
        for reader in readers:
            reader_short = str(reader)[-4:]  # Shorten UUID
            # Highlight the specified visitor if it is among the shared readers
            if visitor_uuid and reader == visitor_uuid:
                graph.node(
                    reader_short, 
                    label=reader_short, 
                    shape="box", 
                    style="filled", 
                    color="lightgreen"
                )
            else:
                graph.node(reader_short, label=reader_short, shape="box")

            # Add edge from the reader to the input document
            edge_to_input = (reader_short, str(doc_uuid)[-4:])
            if edge_to_input not in added_edges:
                graph.edge(*edge_to_input)
                added_edges.add(edge_to_input)

            # Add edge from the reader to the related document
            edge_to_related = (reader_short, str(related_doc)[-4:])
            if edge_to_related not in added_edges:
                graph.edge(*edge_to_related)
                added_edges.add(edge_to_related)

    # Save and display the graph
    output_base_path = f"also_likes_{str(doc_uuid)[-4:]}"
    png_output_path = graph.render(output_base_path, format='png')

    # Display the generated graph as an image
    img = Image.open(png_output_path)
    plt.figure(figsize=(12, 8))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

    print(f"Graph generated and saved to: {png_output_path}")
