import pandas as pd

if __name__ == "__main__":
    # Load the JSON file into a DataFrame
    file_path = r'C:\Users\Anmole\Downloads\sample_tiny.json'
    with open(file_path, 'r') as file:
        data = pd.read_json(file, lines=True)

    # Filter the required columns
    data = data[['subject_doc_id', 'visitor_uuid']]

    # Find overlapping readers for documents
    overlaps = data.groupby('visitor_uuid')['subject_doc_id'].nunique()
    overlapping_readers = overlaps[overlaps > 1]
    print("Readers who read multiple documents:")
    print(overlapping_readers)

    # Find documents read by these readers
    common_docs = data[data['visitor_uuid'].isin(overlapping_readers.index)]
    print("\nDocuments read by readers with multiple interactions:")
    print(common_docs['subject_doc_id'].unique())
