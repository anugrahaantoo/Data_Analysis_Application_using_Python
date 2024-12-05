import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from also_likes import generate_also_likes_graph, also_likes
from data_analysis import load_data
from reader_analysis import analyze_top_readers
from visualization import generate_country_histogram, generate_continent_histogram, generate_main_browser_histogram

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analytics")
        self.geometry("1200x500")

        # Input for file path and document UUID
        self.file_path_label = tk.Label(self, text="Select dataset file:")
        self.file_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.file_path_entry = tk.Entry(self, width=40)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=5)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Load Data button below the first row of inputs
        self.load_button = tk.Button(self, text="Load Data", command=self.load_data)
        self.load_button.grid(row=1, column=1, padx=5, pady=5)

        self.doc_uuid_label = tk.Label(self, text="Enter Document UUID:")
        self.doc_uuid_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.doc_uuid_entry = tk.Entry(self, width=40)
        self.doc_uuid_entry.grid(row=2, column=1, padx=10, pady=5)

        # Visitor ID Input
        self.visitor_id_label = tk.Label(self, text="Enter Visitor ID (Optional):")
        self.visitor_id_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")

        self.visitor_id_entry = tk.Entry(self, width=40)
        self.visitor_id_entry.grid(row=2, column=3, padx=10, pady=5)

        # Set a uniform width for all buttons
        button_width = 30  # Adjust this value as needed

        # Buttons for generating reports, using grid layout
        self.generate_browser_button = tk.Button(self, text="Generate Browser Histogram", command=self.generate_browser_histogram, width=button_width)
        self.generate_browser_button.grid(row=5, column=1, pady=5)

        self.generate_country_button = tk.Button(self, text="Generate Country Histogram", command=self.generate_country_histogram, width=button_width)
        self.generate_country_button.grid(row=6, column=1, pady=5)

        self.generate_continent_button = tk.Button(self, text="Generate Continent Histogram", command=self.generate_continent_histogram, width=button_width)
        self.generate_continent_button.grid(row=7, column=1, pady=5)

        self.generate_top10_button = tk.Button(self, text="Top 10 Readers", command=self.generate_analyze_top_readers, width=button_width)
        self.generate_top10_button.grid(row=4, column=2, pady=5)

        self.generate_also_likes_button = tk.Button(self, text="Generate 'Also Likes' List", command=self.generate_also_likes, width=button_width)
        self.generate_also_likes_button.grid(row=4, column=3, pady=5)

        self.generate_also_likes_graph_button = tk.Button(self, text="Generate 'Also Likes' Graph", command=self.generate_also_likes_graph, width=button_width)
        self.generate_also_likes_graph_button.grid(row=8, column=1, pady=5)

        # Top Readers Frame with Table
        self.top_readers_frame = tk.Frame(self)
        self.top_readers_frame.grid(row=5, column=2, rowspan=10, padx=10, pady=5, sticky="ns")

        self.top_readers_label = tk.Label(self.top_readers_frame, text="Top 10 Readers:")
        self.top_readers_label.grid(row=0, column=0, pady=5, sticky="w")

        self.top_readers_table = ttk.Treeview(self.top_readers_frame, columns=("UUID", "Time"), show="headings", height=10)
        self.top_readers_table.heading("UUID", text="Visitor UUID")
        self.top_readers_table.heading("Time", text="Time Spent (seconds)")
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



    def browse_file(self):
        """
        Opens a file dialog to select a file and updates the file path entry field.
        """
        file_path = filedialog.askopenfilename(title="Select a Dataset File", filetypes=[("JSON Files", "*.json;*.gz")])
        if file_path:
            self.file_path_entry.delete(0, tk.END)  # Clear any previous entry
            self.file_path_entry.insert(0, file_path)  # Insert the selected file path

    def load_data(self):
        file_path = self.file_path_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a dataset file.")
            return
        self.df = load_data(file_path)

    def generate_browser_histogram(self):
        if hasattr(self, 'df'):
            generate_main_browser_histogram(self.df)
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    def generate_country_histogram(self):
        doc_uuid = self.doc_uuid_entry.get()
        if hasattr(self, 'df'):
            generate_country_histogram(self.df, doc_uuid)
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    def generate_continent_histogram(self):
        doc_uuid = self.doc_uuid_entry.get()
        continent_mapping = {
            "US": "North America", "CA": "North America", "MX": "North America",
            "BR": "South America", "AR": "South America", "CL": "South America", "CO": "South America", "PE": "South America",
            "DE": "Europe", "FR": "Europe", "IT": "Europe", "ES": "Europe", "GB": "Europe", "RU": "Europe",
            "PL": "Europe", "SE": "Europe", "NL": "Europe", "BE": "Europe", "AT": "Europe", "CH": "Europe",
            "IN": "Asia", "CN": "Asia", "JP": "Asia", "KR": "Asia", "SG": "Asia", "MY": "Asia", "ID": "Asia",
            "TH": "Asia", "PH": "Asia", "VN": "Asia", "PK": "Asia", "BD": "Asia", "IR": "Asia", "IQ": "Asia", "SA": "Asia",
            "ZA": "Africa", "EG": "Africa", "NG": "Africa", "KE": "Africa", "GH": "Africa", "DZ": "Africa",
            "MA": "Africa", "TZ": "Africa", "UG": "Africa", "SN": "Africa", "MW": "Africa", "ZM": "Africa", "MZ": "Africa",
            "AU": "Oceania", "NZ": "Oceania", "FJ": "Oceania", "PG": "Oceania", "WS": "Oceania"
        }
        if hasattr(self, 'df'):
            generate_continent_histogram(self.df, doc_uuid, continent_mapping)
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    def generate_analyze_top_readers(self):
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

    def generate_also_likes(self):
        doc_uuid = self.doc_uuid_entry.get()
        visitor_id = self.visitor_id_entry.get()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return

        if hasattr(self, 'df'):
            try:
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

    def generate_also_likes_graph(self):
        doc_uuid = self.doc_uuid_entry.get()
        visitor_id = self.visitor_id_entry.get()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return

        if hasattr(self, 'df'):
            try:
                if visitor_id:
                    generate_also_likes_graph(self.df, doc_uuid, visitor_id)
                else:
                    generate_also_likes_graph(self.df, doc_uuid)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
