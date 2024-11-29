import tkinter as tk
from tkinter import filedialog
from data_processor import DataProcessor
from visualizer import Visualizer

class DocumentTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Document Tracker")
        self.processor = None

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.processor = DataProcessor(file_path)

    def show_views_by_country(self):
        if not self.processor:
            return
        doc_uuid = self._get_document_uuid()
        data = self.processor.views_by_country(doc_uuid)
        Visualizer.plot_histogram(data, "Views by Country", "Country", "Views")

    def show_views_by_browser(self):
        if not self.processor:
            return
        data = self.processor.views_by_browser()
        Visualizer.plot_histogram(data, "Views by Browser", "Browser", "Views")

    def run(self):
        tk.Button(self.root, text="Load Data", command=self.load_data).pack()
        tk.Button(self.root, text="Views by Country", command=self.show_views_by_country).pack()
        tk.Button(self.root, text="Views by Browser", command=self.show_views_by_browser).pack()
        self.root.mainloop()

    def _get_document_uuid(self):
        return tk.simpledialog.askstring("Input", "Enter Document UUID:")
