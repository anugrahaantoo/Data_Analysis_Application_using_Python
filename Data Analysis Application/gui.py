import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from also_likes import also_likes_graph, also_likes
from data_processing import load_data
from top_readers import analyze_top_readers
from display_histogram import country_histogram, continent_histogram, browser_histogram, detailed_browser_histogram

# map the countries to their respective continents
continent_mapping = {
    # North America
    "US": "North America", "CA": "North America", "MX": "North America", "BM": "North America",
    "BS": "North America", "BZ": "North America", "CR": "North America", "CU": "North America",
    "DO": "North America", "GT": "North America", "HN": "North America", "HT": "North America",
    "JM": "North America", "NI": "North America", "PA": "North America", "PR": "North America",
    "SV": "North America", "TT": "North America",

    # South America
    "AR": "South America", "BO": "South America", "BR": "South America", "CL": "South America",
    "CO": "South America", "EC": "South America", "GY": "South America", "PE": "South America",
    "PY": "South America", "SR": "South America", "UY": "South America", "VE": "South America",

    # Europe
    "AL": "Europe", "AD": "Europe", "AT": "Europe", "BY": "Europe", "BE": "Europe", "BA": "Europe",
    "BG": "Europe", "HR": "Europe", "CY": "Europe", "CZ": "Europe", "DK": "Europe", "EE": "Europe",
    "FI": "Europe", "FR": "Europe", "DE": "Europe", "GR": "Europe", "HU": "Europe", "IS": "Europe",
    "IE": "Europe", "IT": "Europe", "LV": "Europe", "LI": "Europe", "LT": "Europe", "LU": "Europe",
    "MT": "Europe", "MD": "Europe", "MC": "Europe", "ME": "Europe", "NL": "Europe", "NO": "Europe",
    "PL": "Europe", "PT": "Europe", "RO": "Europe", "RU": "Europe", "SM": "Europe", "RS": "Europe",
    "SK": "Europe", "SI": "Europe", "ES": "Europe", "SE": "Europe", "CH": "Europe", "TR": "Europe",
    "UA": "Europe", "GB": "Europe", "VA": "Europe",

    # Asia
    "AF": "Asia", "AM": "Asia", "AZ": "Asia", "BH": "Asia", "BD": "Asia", "BT": "Asia", "BN": "Asia",
    "KH": "Asia", "CN": "Asia", "CY": "Asia", "GE": "Asia", "IN": "Asia", "ID": "Asia", "IR": "Asia",
    "IQ": "Asia", "IL": "Asia", "JP": "Asia", "JO": "Asia", "KZ": "Asia", "KW": "Asia", "KG": "Asia",
    "LA": "Asia", "LB": "Asia", "MY": "Asia", "MV": "Asia", "MN": "Asia", "MM": "Asia", "NP": "Asia",
    "OM": "Asia", "PK": "Asia", "PH": "Asia", "QA": "Asia", "SA": "Asia", "SG": "Asia", "KR": "Asia",
    "LK": "Asia", "SY": "Asia", "TJ": "Asia", "TH": "Asia", "TL": "Asia", "TM": "Asia", "AE": "Asia",
    "UZ": "Asia", "VN": "Asia", "YE": "Asia",

    # Africa
    "DZ": "Africa", "AO": "Africa", "BJ": "Africa", "BW": "Africa", "BF": "Africa", "BI": "Africa",
    "CM": "Africa", "CV": "Africa", "CF": "Africa", "TD": "Africa", "KM": "Africa", "CG": "Africa",
    "DJ": "Africa", "EG": "Africa", "GQ": "Africa", "ER": "Africa", "SZ": "Africa", "ET": "Africa",
    "GA": "Africa", "GM": "Africa", "GH": "Africa", "GN": "Africa", "GW": "Africa", "CI": "Africa",
    "KE": "Africa", "LS": "Africa", "LR": "Africa", "MG": "Africa", "MW": "Africa", "ML": "Africa",
    "MR": "Africa", "MU": "Africa", "MA": "Africa", "MZ": "Africa", "NA": "Africa", "NE": "Africa",
    "NG": "Africa", "RW": "Africa", "ST": "Africa", "SN": "Africa", "SC": "Africa", "SL": "Africa",
    "SO": "Africa", "ZA": "Africa", "SS": "Africa", "SD": "Africa", "TZ": "Africa", "TG": "Africa",
    "TN": "Africa", "UG": "Africa", "ZM": "Africa", "ZW": "Africa",

    # Oceania
    "AU": "Oceania", "FJ": "Oceania", "KI": "Oceania", "MH": "Oceania", "FM": "Oceania", "NR": "Oceania",
    "NZ": "Oceania", "PW": "Oceania", "PG": "Oceania", "WS": "Oceania", "SB": "Oceania", "TO": "Oceania",
    "TV": "Oceania", "VU": "Oceania",

    # Antarctica
    "AQ": "Antarctica"
}

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analytics")
        self.geometry("1200x500")

        #label and field to enter the dataset file path
        self.file_path_label = tk.Label(self, text="Select dataset file:")
        self.file_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.file_path_entry = tk.Entry(self, width=40)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=5)

        #Browse button
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Load Data button 
        self.load_button = tk.Button(self, text="Load Data", command=self.load_data)
        self.load_button.grid(row=1, column=1, padx=5, pady=5)

        #Label and field to enter the document id
        self.doc_uuid_label = tk.Label(self, text="Enter Document UUID:")
        self.doc_uuid_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.doc_uuid_entry = tk.Entry(self, width=40)
        self.doc_uuid_entry.grid(row=2, column=1, padx=10, pady=5)

        # Label and field to enter the Visitor ID 
        self.visitor_id_label = tk.Label(self, text="Enter Visitor ID (Optional):")
        self.visitor_id_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")

        self.visitor_id_entry = tk.Entry(self, width=40)
        self.visitor_id_entry.grid(row=2, column=3, padx=10, pady=5)

        # Set a uniform width for all buttons
        button_width = 30  

        # Buttons for generating histograms, top 10 readers and also likes list
        self.detailed_browser_button = tk.Button(self, text="Detailed Browser Histogram ", command=self.detailed_browser_histogram, width=button_width)
        self.detailed_browser_button.grid(row=5, column=1, pady=5)

        self.browser_button = tk.Button(self, text="Browser Histogram", command=self.browser_histogram, width=button_width)
        self.browser_button.grid(row=6, column=1, pady=5)

        self.country_button = tk.Button(self, text="Country Histogram", command=self.country_histogram, width=button_width)
        self.country_button.grid(row=7, column=1, pady=5)

        self.continent_button = tk.Button(self, text="Continent Histogram", command=self.continent_histogram, width=button_width)
        self.continent_button.grid(row=8, column=1, pady=5)

        self.top10_button = tk.Button(self, text="Top 10 Readers", command=self.analyze_top_readers, width=button_width)
        self.top10_button.grid(row=4, column=2, pady=5)

        self.also_likes_button = tk.Button(self, text="'Also Likes' List", command=self.also_likes, width=button_width)
        self.also_likes_button.grid(row=4, column=3, pady=5)

        self.also_likes_graph_button = tk.Button(self, text="'Also Likes' Graph", command=self.also_likes_graph, width=button_width)
        self.also_likes_graph_button.grid(row=9, column=1, pady=5)

        # Top Readers Frame with Table
        self.top_readers_frame = tk.Frame(self)
        self.top_readers_frame.grid(row=5, column=2, rowspan=10, padx=10, pady=5, sticky="ns")

        self.top_readers_label = tk.Label(self.top_readers_frame, text="Top 10 Readers:")
        self.top_readers_label.grid(row=0, column=0, pady=5, sticky="w")

        self.top_readers_table = ttk.Treeview(self.top_readers_frame, columns=("UUID", "Time"), show="headings", height=10)
        self.top_readers_table.heading("UUID", text="Visitor UUID")
        self.top_readers_table.heading("Time", text="Time Spent (ms)")
        self.top_readers_table.column("UUID", width=230, anchor="w")
        self.top_readers_table.column("Time", width=120, anchor="center")
        self.top_readers_table.grid(row=1, column=0, sticky="nsew")

        # Also Likes Frame with Table
        self.also_likes_frame = tk.Frame(self)
        self.also_likes_frame.grid(row=5, column=3, rowspan=10, padx=10, pady=5, sticky="ns")

        self.also_likes_label = tk.Label(self.also_likes_frame, text="Also Likes:")
        self.also_likes_label.grid(row=0, column=0, pady=5, sticky="w")

        self.also_likes_table = ttk.Treeview(self.also_likes_frame, columns=("Document_UUID",), show="headings", height=10)
        self.also_likes_table.heading("Document_UUID", text="Document UUID")
        self.also_likes_table.column("Document_UUID", width=350, anchor="w")
        self.also_likes_table.grid(row=1, column=0, sticky="nsew")


    
    #file dialog to select a file for loading data
    def browse_file(self):
        
        file_path = filedialog.askopenfilename(title="Select a Dataset File", filetypes=[("JSON Files", "*.json;*.gz")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)  # Clear any previous entry
            self.file_path_entry.insert(0, file_path)  # Insert the selected file path

    #loads the data by taking the file path
    def load_data(self):
        file_path = self.file_path_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a dataset file.")
            return
        self.df = load_data(file_path)
        # Check if the dataframe is not empty
        if self.df is not None and not self.df.empty:
            messagebox.showinfo("Success", "Data Loaded Successfully")
            
        else:
            messagebox.showerror("Error", "The file is empty or invalid.")
    
    #method to display the detailed browser histogram
    def detailed_browser_histogram(self):
        if hasattr(self, 'df'):
            detailed_browser_histogram(self.df)
        else:
            messagebox.showerror("Error", "Data not loaded yet.")
   
   #method to display the browser histogram
    def browser_histogram(self):
        
        if hasattr(self, 'df'):
            browser_histogram(self.df)
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    #method to display the country histogram based on the document id
    def country_histogram(self):
        doc_uuid = self.doc_uuid_entry.get()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return
        if hasattr(self, 'df'):
            country_histogram(self.df, doc_uuid)
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    #method to display the continent histogram based on the document id
    def continent_histogram(self):
        doc_uuid = self.doc_uuid_entry.get()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return
        if hasattr(self, 'df'):
            continent_histogram(self.df, doc_uuid, continent_mapping)
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    #method to get the top readers for the 
    def analyze_top_readers(self):
        if hasattr(self, 'df'):
            top_readers_list = analyze_top_readers(self.df)
            if top_readers_list:
                # Clear existing rows
                for item in self.top_readers_table.get_children():
                    self.top_readers_table.delete(item)

                # Insert new rows
                for i, reader in enumerate(top_readers_list):
                    uuid, time = reader.split(" : ")
                    self.top_readers_table.insert("", "end", values=(uuid, time))
            else:
                messagebox.showinfo("Info", "No top readers found.")
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    #method to display the also likes list based on the document id and visitor id entered
    def also_likes(self):
        doc_uuid = self.doc_uuid_entry.get()
        visitor_id = self.visitor_id_entry.get()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return

        if hasattr(self, 'df'):
            try:
                #check is the user entered the visitor id
                if visitor_id:
                    also_likes_list = also_likes(self.df, doc_uuid, visitor_id)
                else:
                    also_likes_list = also_likes(self.df, doc_uuid)

                if also_likes_list:
                    # Clear existing rows
                    for item in self.also_likes_table.get_children():
                        self.also_likes_table.delete(item)

                    # Insert new rows
                    for doc in also_likes_list:
                        self.also_likes_table.insert("", "end", values=(doc,))
                else:
                    messagebox.showinfo("Info", "No 'also liked' documents found.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    #method to display the also likes graph
    def also_likes_graph(self):
        doc_uuid = self.doc_uuid_entry.get()
        visitor_id = self.visitor_id_entry.get()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return

        if hasattr(self, 'df'):
            try:
                if visitor_id:
                    also_likes_graph(self.df, doc_uuid, visitor_id)
                else:
                    also_likes_graph(self.df, doc_uuid)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
