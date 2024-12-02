# gui.py
import tkinter as tk
from tkinter import messagebox
from data_analysis import load_data, also_likes, generate_also_likes_graph
from visualization import generate_country_histogram, generate_continent_histogram, generate_main_browser_histogram

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analytics")
        self.geometry("500x400")

        # Input for file path and document UUID
        self.file_path_label = tk.Label(self, text="Enter dataset file path:")
        self.file_path_label.pack()
        self.file_path_entry = tk.Entry(self, width=50)
        self.file_path_entry.pack()

        self.doc_uuid_label = tk.Label(self, text="Enter Document UUID:")
        self.doc_uuid_label.pack()
        self.doc_uuid_entry = tk.Entry(self, width=50)
        self.doc_uuid_entry.pack()

        # Buttons for generating reports
        self.load_button = tk.Button(self, text="Load Data", command=self.load_data)
        self.load_button.pack()

        self.generate_browser_button = tk.Button(self, text="Generate Browser Histogram", command=self.generate_browser_histogram)
        self.generate_browser_button.pack()

        self.generate_country_button = tk.Button(self, text="Generate Country Histogram", command=self.generate_country_histogram)
        self.generate_country_button.pack()

        self.generate_continent_button = tk.Button(self, text="Generate Continent Histogram", command=self.generate_continent_histogram)
        self.generate_continent_button.pack()

        self.generate_also_likes_button = tk.Button(self, text="Generate 'Also Likes' List", command=self.generate_also_likes)
        self.generate_also_likes_button.pack()

    def load_data(self):
        file_path = self.file_path_entry.get()
        self.df = load_data(file_path)
        if self.df is not None:
            messagebox.showinfo("Success", "Data Loaded Successfully")

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

    def generate_also_likes(self):
        doc_uuid = self.doc_uuid_entry.get()
        if hasattr(self, 'df'):
            also_likes_list = also_likes(self.df, doc_uuid)
            messagebox.showinfo("Also Likes", ", ".join(also_likes_list))
        else:
            messagebox.showerror("Error", "Data not loaded yet.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
