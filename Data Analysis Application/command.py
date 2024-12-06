import argparse
import matplotlib.pyplot as plt
from data_processing import load_data   #function to load data from JSON
from top_readers import analyze_top_readers     #function to analyze top readers
from display_histogram import country_histogram, continent_histogram, detailed_browser_histogram, browser_histogram 
from also_likes import also_likes_graph, also_likes     #function for also like
from gui import Application  #GUI class to lauch the GUI interface   
from gui import continent_mapping # to map countries to contients

#Plotting histogram of countries of the viewers
def run_task_2a(file_name, doc_uuid):
    
    #load data from JSON file
    df = load_data(file_name)
    if df is not None:
        country_histogram(df, doc_uuid)  # plotting using filtered data
    else:
        print("Failed to load data for Task 2a.")


# plotting histogram of continents of the viewers 
def run_task_2b(file_name, doc_uuid):
    
    df = load_data(file_name)
    if df is not None:
        print("Data Loaded Successfully! ")
        try:
            #  directly use the filtered data and continent mapping
            continent_histogram(df, doc_uuid, continent_mapping)
            print("Continent histogram generated successfully.")
        except Exception as e:
            print(f"Error generating continent histogram: {e}")
    else:
        print("Failed to load data for Task 2b.")

# plotting histogram of browser names along with OS details  
def run_task_3a(file_name):
    
    df = load_data(file_name)
    
    df = load_data(file_name)
    if df is not None:
        detailed_browser_histogram(df)
    else:
        print("Failed to load data for Task 3a.")
#plotting a histogram of main  browser names 
def run_task_3b(file_name):
   
    df = load_data(file_name)
    if df is not None:
        browser_histogram(df)
    else:
        print("Failed to load data for Task 3b.")

#Top 10 readers
def run_task_4(file_name):
    
    df = load_data(file_name)
    if df is not None:
        print("Data Loaded Successfully! ")
        top_readers = analyze_top_readers(df)
        
        print("Top 10 Readers:")
        for reader in top_readers:
            print(reader)
    else:
        print("Failed to load data for Task 4.")

#printing Also likes list
def run_task_5d(file_name, doc_uuid):
   
    df = load_data(file_name)
    if df is not None:
        print("Data Loaded Successfully! ")
        liked_docs = also_likes(df, doc_uuid)   #get the top 10 liked documents
        print("Top 10 Also like\n")
        for doc in liked_docs:
            print(doc)
    else:
        print("Failed to load data for Task 5d.")

#generating also like graph
def run_task_6( file_name,doc_uuid,visitor_uuid=None):
    """Task 6: Generate 'Also Likes' graph."""
    df = load_data(file_name)
    if df is not None:
        also_likes_graph(df, doc_uuid,visitor_uuid)
    else:
        print("Failed to load data for Task 6.")

#running task 6 and launching GUI
def run_task_7():
    
    print("Launching the GUI...")
    app = Application() #create GUI application instance
    app.mainloop()

def main():
    # argument parsing for command-line input
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
            run_task_2b(args.file_name, args.doc_uuid) 
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

#calling main function to start program
if __name__ == "__main__":
    main()
