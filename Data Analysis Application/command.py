import argparse
from data_analysis import load_data
from reader_analysis import analyze_top_readers
from visualization import generate_country_histogram, generate_continent_histogram, generate_detailed_browser_histogram, generate_browser_histogram 
from also_likes import generate_also_likes_graph, also_likes
from gui import Application
from gui import continent_mapping 


def run_task_2a(file_name, doc_uuid):
    """Task 2a: Generate a histogram of countries of the viewers."""
    df = load_data(file_name)
    if df is not None:
        generate_country_histogram(df, doc_uuid)  # Pass the required doc_uuid
    else:
        print("Failed to load data for Task 2a.")



def run_task_2b(file_name, doc_uuid):
    """Task 2b: Generate a histogram of continents of the viewers."""
    df = load_data(file_name)
    if df is not None:
        print("Data Loaded Successfully! ")
        try:
            # Now we can directly use the continent_mapping imported from gui.py
            generate_continent_histogram(df, doc_uuid, continent_mapping)
            print("Continent histogram generated successfully.")
        except Exception as e:
            print(f"Error generating continent histogram: {e}")
    else:
        print("Failed to load data for Task 2b.")

def run_task_3a(file_name):
    """
    Task 3a: Display a histogram of browser names with descriptions (OS details).
    """
    df = load_data(file_name)
    
    df = load_data(file_name)
    if df is not None:
        generate_detailed_browser_histogram(df)
    else:
        print("Failed to load data for Task 3a.")

def run_task_3b(file_name):
    """
    Task 3b: Display a histogram of all browser identifiers of the viewers.
    """
    df = load_data(file_name)
    if df is not None:
        generate_browser_histogram(df)
    else:
        print("Failed to load data for Task 3b.")

def run_task_4(file_name):
    """Task 4: Analyze and return the top 10 readers."""
    df = load_data(file_name)
    if df is not None:
        print("Data Loaded Successfully! ")
        top_readers = analyze_top_readers(df)
        
        print("Top 10 Readers:")
        for reader in top_readers:
            print(reader)
    else:
        print("Failed to load data for Task 4.")


def run_task_5d(doc_uuid, file_name):
    """Task 5d: Generate 'Also Likes' list."""
    df = load_data(file_name)
    if df is not None:
        print("Data Loaded Successfully! ")
        liked_docs = also_likes(df, doc_uuid)
        print("Top 10 Also like\n")
        for doc in liked_docs:
            print(doc)
    else:
        print("Failed to load data for Task 5d.")


def run_task_6( file_name,doc_uuid,visitor_uuid=None):
    """Task 6: Generate 'Also Likes' graph."""
    df = load_data(file_name)
    if df is not None:
        generate_also_likes_graph(df, doc_uuid,visitor_uuid)
    else:
        print("Failed to load data for Task 6.")


def run_task_7():
    """Task 7: Run Task 6 and launch the GUI."""
    print("Launching the GUI...")
    app = Application()
    app.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Command-line tool for testing tasks")
    parser.add_argument('-u', '--user_uuid', help="User UUID (not required for all tasks)")
    parser.add_argument('-d', '--doc_uuid', help="Document UUID (required for some tasks)")
    parser.add_argument('-v', '--visitor_uuid', help="Visitor UUID (required for some tasks)")
    parser.add_argument('-t', '--task_id', required=True, help="Task ID")
    parser.add_argument('-f', '--file_name', required=True, help="Input JSON file")

    args = parser.parse_args()

    # Match task ID and call corresponding function
    if args.task_id == '2a':
        if args.doc_uuid:
            run_task_2a(args.file_name, args.doc_uuid)
        else:
            print("Error: Task 2a requires a Document UUID.")
    elif args.task_id == '2b':
        if args.doc_uuid:
            run_task_2b(args.file_name, args.doc_uuid)  # Pass doc_uuid to run_task_2b
        else:
            print("Error: Task 2b requires a Document UUID.")
    elif args.task_id == '3a':
        run_task_3a(args.file_name)
    elif args.task_id == '3b':
        run_task_3b(args.file_name)
    elif args.task_id == '4':
        run_task_4(args.file_name)
    elif args.task_id == '5d':
        if args.doc_uuid:
            run_task_5d( args.file_name,args.doc_uuid)
        else:
            print("Error: Task 5 requires a Document UUID.")
    elif args.task_id == '6':
        if args.doc_uuid:
            run_task_6( args.file_name, args.doc_uuid,args.visitor_uuid)
        else:
            print("Error: Task 6 requires a Document UUID.")
    elif args.task_id == '7':
        run_task_7()
    else:
        print(f"Invalid task ID: {args.task_id}")


if __name__ == "__main__":
    main()
