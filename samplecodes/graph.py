import graphviz
from collections import defaultdict

def generate_also_likes_graph(input_doc_uuid, input_reader_uuid, also_like_documents, reader_to_docs):
    """
    Generates a graph in .dot format and visualizes it using Graphviz.
    
    :param input_doc_uuid: UUID of the input document (string)
    :param input_reader_uuid: UUID of the input reader (string)
    :param also_like_documents: List of "also like" document UUIDs (list)
    :param reader_to_docs: Dictionary mapping reader UUIDs to their document UUIDs (dict)
    """
    # Shorten UUIDs to the last 4 hex digits
    shorten = lambda uuid: uuid[-4:]
    input_doc_short = shorten(input_doc_uuid)
    input_reader_short = shorten(input_reader_uuid)

    # Create a Graphviz Digraph
    dot = graphviz.Digraph(format='pdf')
    dot.attr(rankdir='LR')  # Left-to-right layout

    # Highlight the input document and reader
    dot.node(input_doc_short, input_doc_short, style='filled', color='green')
    dot.node(input_reader_short, input_reader_short, style='filled', color='green')

    # Add edges between readers and documents
    for reader, docs in reader_to_docs.items():
        reader_short = shorten(reader)
        for doc in docs:
            doc_short = shorten(doc)
            if doc == input_doc_uuid or doc in also_like_documents:
                dot.node(doc_short, doc_short)
                dot.node(reader_short, reader_short)
                dot.edge(reader_short, doc_short)

    # Render the graph to a file
    output_file = "also_likes_graph"
    dot.render(output_file, cleanup=True)
    print(f"Graph saved as {output_file}.pdf")

# Example Usage
input_doc_uuid = "123e4567-e89b-12d3-a456-426614174000"
input_reader_uuid = "abcdef12-3456-7890-abcd-ef1234567890"
also_like_documents = ["456e1234-e89b-12d3-a456-426614174111", "789a1234-e89b-12d3-a456-426614174222"]
reader_to_docs = {
    "abcdef12-3456-7890-abcd-ef1234567890": [
        "123e4567-e89b-12d3-a456-426614174000",
        "456e1234-e89b-12d3-a456-426614174111",
    ],
    "12345678-abcd-1234-abcd-1234567890ab": [
        "789a1234-e89b-12d3-a456-426614174222",
        "123e4567-e89b-12d3-a456-426614174000",
    ],
}

generate_also_likes_graph(input_doc_uuid, input_reader_uuid, also_like_documents, reader_to_docs)
