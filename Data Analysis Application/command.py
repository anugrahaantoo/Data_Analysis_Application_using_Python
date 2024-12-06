import argparse
from data_analysis import load_data, also_likes
from reader_analysis import analyze_top_readers
from visualization import generate_country_histogram, generate_continent_histogram, generate_main_browser_histogram
from also_likes import generate_also_likes_graph
from gui import Application


def run_task_2a(file_name, doc_uuid):
    """Task 2a: Generate a histogram of countries of the viewers."""
    df = load_data(file_name)
    if df is not None:
        generate_country_histogram(df, doc_uuid)  # Pass the required doc_uuid
    else:
        print("Failed to load data for Task 2a.")


def run_task_2b(file_name):
    """Task 2b: Generate a histogram of continents of the viewers."""
    df = load_data(file_name)
    if df is not None:
        generate_continent_histogram(df)
    else:
        print("Failed to load data for Task 2b.")


def run_task_3a(file_name):
    """Task 3a: Display a histogram of all browser identifiers of the viewers."""
    df = load_data(file_name)
    if df is not None:
        generate_main_browser_histogram(df)
    else:
        print("Failed to load data for Task 3a.")


def run_task_3b(file_name):
    """Task 3b: Display a histogram of main browser names."""
    df = load_data(file_name)
    if df is not None:
        df['main_browser'] = df['browser_id'].apply(lambda x: extract_browser_name(x))
        generate_main_browser_histogram(df)
    else:
        print("Failed to load data for Task 3b.")


def run_task_4(file_name):
    """Task 4: Analyze and return the top 10 readers."""
    df = load_data(file_name)
    if df is not None:
        top_readers = analyze_top_readers(df)
        print("Top 10 Readers:")
        for reader in top_readers:
            print(reader)
    else:
        print("Failed to load data for Task 4.")


def run_task_5(doc_uuid, file_name):
    """Task 5: Generate 'Also Likes' list."""
    df = load_data(file_name)
    if df is not None:
        liked_docs = also_likes(df, doc_uuid)
        print(f"Also Likes for document {doc_uuid}: {liked_docs}")
    else:
        print("Failed to load data for Task 5.")


def run_task_6(doc_uuid, file_name):
    """Task 6: Generate 'Also Likes' graph."""
    df = load_data(file_name)
    if df is not None:
        generate_also_likes_graph(df, doc_uuid)
    else:
        print("Failed to load data for Task 6.")


def run_task_7(file_name):
    """Task 7: Run Task 6 and launch the GUI."""
    print("Launching the GUI...")
    app = Application()
    app.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Command-line tool for testing tasks")
    parser.add_argument('-u', '--user_uuid', help="User UUID (not required for all tasks)")
    parser.add_argument('-d', '--doc_uuid', help="Document UUID (required for some tasks)")
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
        run_task_2b(args.file_name)
    elif args.task_id == '3a':
        run_task_3a(args.file_name)
    elif args.task_id == '3b':
        run_task_3b(args.file_name)
    elif args.task_id == '4':
        run_task_4(args.file_name)
    elif args.task_id == '5':
        if args.doc_uuid:
            run_task_5(args.doc_uuid, args.file_name)
        else:
            print("Error: Task 5 requires a Document UUID.")
    elif args.task_id == '6':
        if args.doc_uuid:
            run_task_6(args.doc_uuid, args.file_name)
        else:
            print("Error: Task 6 requires a Document UUID.")
    elif args.task_id == '7':
        run_task_7(args.file_name)
    else:
        print(f"Invalid task ID: {args.task_id}")


if __name__ == "__main__":
    main()
