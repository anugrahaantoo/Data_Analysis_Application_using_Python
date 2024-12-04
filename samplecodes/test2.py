import pandas as pd

# Load the JSON file into a DataFrame
file_path = r'C:\Users\Anmole\Downloads\sample_tiny.json'
data = pd.read_json(file_path, lines=True)

# Filter required columns
data = data[['subject_doc_id', 'visitor_uuid']]

# Find documents with multiple readers
doc_reader_counts = data.groupby('subject_doc_id')['visitor_uuid'].nunique()
suitable_docs = doc_reader_counts[doc_reader_counts > 1]

print("Documents with multiple readers:")
print(suitable_docs)
