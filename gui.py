import tkinter as tk
from tkinter import messagebox, filedialog
import dask.dataframe as dd
from data_analysis import load_data, also_likes, generate_also_likes_graph
from reader_analysis import analyze_top_readers
from visualization import generate_country_histogram, generate_continent_histogram, generate_main_browser_histogram

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analytics")
        self.geometry("600x300")

        # Input for file path and document UUID
        self.file_path_label = tk.Label(self, text="Select dataset file:")
        self.file_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.file_path_entry = tk.Entry(self, width=40)
        self.file_path_entry.grid(row=0, column=1, padx=10, pady=5)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        # Load Data button below the first row of inputs
        self.load_button = tk.Button(self, text="Load Data", command=self.load_data)
        self.load_button.grid(row=0, column=3, padx=10, pady=5)

        self.doc_uuid_label = tk.Label(self, text="Enter Document UUID:")
        self.doc_uuid_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.doc_uuid_entry = tk.Entry(self, width=40)
        self.doc_uuid_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons for generating reports, using grid layout
        self.generate_browser_button = tk.Button(self, text="Generate Browser Histogram", command=self.generate_browser_histogram)
        self.generate_browser_button.grid(row=3, column=0, columnspan=4, pady=5)

        self.generate_country_button = tk.Button(self, text="Generate Country Histogram", command=self.generate_country_histogram)
        self.generate_country_button.grid(row=4, column=0, columnspan=4, pady=5)

        self.generate_continent_button = tk.Button(self, text="Generate Continent Histogram", command=self.generate_continent_histogram)
        self.generate_continent_button.grid(row=5, column=0, columnspan=4, pady=5)

        self.generate_top10_button = tk.Button(self, text="Top 10 Readers", command=self.generate_analyze_top_readers)
        self.generate_top10_button.grid(row=6, column=0, columnspan=4, pady=5)

        self.generate_also_likes_button = tk.Button(self, text="Generate 'Also Likes' List", command=self.generate_also_likes)
        self.generate_also_likes_button.grid(row=7, column=0, columnspan=4, pady=5)

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
        # Corrected ISO3166 two-letter country code to continent mapping
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
            messagebox.showinfo("Top 10 Readers", "\n ".join(top_readers_list))
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

    def generate_also_likes(self):
        """
        Generate and display the 'also likes' list for the given document UUID.
        """
        doc_uuid = self.doc_uuid_entry.get()  # Get the input document UUID from the GUI
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return

        if hasattr(self, 'df'):
            try:
                # Generate the 'also likes' list using the also_likes function
                also_likes_list = also_likes(self.df, doc_uuid)
                
                # Display the result in a message box
                if also_likes_list:
                    messagebox.showinfo("Also Likes", "Top 10 'Also Liked' Documents:\n" + ", ".join(also_likes_list))
                else:
                    messagebox.showinfo("Also Likes", "No 'also liked' documents found for the given Document UUID.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Data not loaded yet.")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
