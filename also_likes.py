import graphviz

def also_likes_list(data, doc_id):
    """Display a list of top documents also liked by readers of the given document."""
    readers = data[data['subject_doc_id'] == doc_id]['visitor_uuid']
    liked_docs = data[data['visitor_uuid'].isin(readers)]['subject_doc_id'].value_counts()
    print(liked_docs.head(10))

def generate_graph(data, doc_id):
    """Generate a Graphviz graph showing relationships between readers and documents."""
    readers = data[data['subject_doc_id'] == doc_id]['visitor_uuid']
    liked_docs = data[data['visitor_uuid'].isin(readers)]
    dot = graphviz.Digraph()

    dot.node(doc_id[-4:], style='filled', color='green')
    for _, row in liked_docs.iterrows():
        reader_id = row['visitor_uuid'][-4:]
        doc_id = row['subject_doc_id'][-4:]
        dot.node(reader_id, shape='circle')
        dot.node(doc_id, shape='box')
        dot.edge(reader_id, doc_id)

    dot.render('also_likes_graph', format='pdf', cleanup=True)
