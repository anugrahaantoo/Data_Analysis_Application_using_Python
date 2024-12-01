import tkinter as tk
import pandas as pd
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from data_processing import load_data
from analysis import get_country_histogram, get_browser_histogram
from also_likes import also_likes_list, generate_graph
from readership_analysis import top_readers
from view_analysis import analyze_views_by_country, analyze_views_by_continent

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Analysis Application")
        self.geometry("500x500")

        self.data = None
        self.create_widgets()

    def create_widgets(self):
        btn_load = tk.Button(self, text="Load JSON File", command=self.load_file)
        btn_load.pack(pady=10)

        tk.Label(self, text="Document UUID:").pack()
        self.doc_uuid_entry = tk.Entry(self, width=30)
        self.doc_uuid_entry.pack(pady=5)

        btn_country_hist = tk.Button(self, text="Country Histogram", command=self.display_country_histogram)
        btn_country_hist.pack(pady=10)

        btn_browser_hist = tk.Button(self, text="Browser Histogram", command=self.display_browser_histogram)
        btn_browser_hist.pack(pady=10)

        btn_top_readers = tk.Button(self, text="Top Readers", command=self.display_top_readers)
        btn_top_readers.pack(pady=10)

        btn_generate_graph = tk.Button(self, text="Generate Also Likes Graph", command=self.generate_also_likes_graph)
        btn_generate_graph.pack(pady=10)

        self.label_status = tk.Label(self, text="Status: Waiting for input...", fg="blue")
        self.label_status.pack(pady=20)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        try:
            self.data = load_data(file_path)
            self.label_status.config(text="Data loaded successfully!", fg="green")
        except Exception as e:
            self.label_status.config(text=f"Error loading data: {e}", fg="red")

    def display_country_histogram(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded!")
            return
        doc_uuid = self.doc_uuid_entry.get().strip()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return
        try:
            # Check if data is a DataFrame and has the 'document_uuid' column
            if not isinstance(self.data, pd.DataFrame):
                messagebox.showerror("Error", "Data is not a valid DataFrame.")
                return
            if 'document_uuid' not in self.data.columns:
                messagebox.showerror("Error", "'document_uuid' column missing in data.")
                return
            histogram = get_country_histogram(self.data, doc_uuid)
            histogram.plot(kind='bar', title='Views by Country')
            plt.xlabel('Country')
            plt.ylabel('Views')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display histogram: {e}")

    def display_browser_histogram(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded!")
            return
        try:
            histogram = get_browser_histogram(self.data)
            histogram.plot(kind='bar', title='Views by Browser')
            plt.xlabel('Browser')
            plt.ylabel('Views')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display histogram: {e}")

    def display_top_readers(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded!")
            return
        try:
            readers = top_readers(self.data)
            print(readers)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display top readers: {e}")

    def generate_also_likes_graph(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded!")
            return
        doc_uuid = self.doc_uuid_entry.get().strip()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a Document UUID.")
            return
        try:
            generate_graph(self.data, doc_uuid)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate graph: {e}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
