#  Data Analysis Application Using Python

A Python-based GUI application designed to analyze user interactions with documents using large-scale data (3M+ records). It combines data analytics, interactive visualizations, and advanced processing tools into a user-friendly interface with both GUI and CLI functionality.

---

## Introduction

In this project, we developed a data analytics application to analyze user interactions with documents. The application features a graphical user interface (GUI) that allows us to load and process interaction data, generate various histograms (e.g., browser, country, and continent), and identify the top 10 readers based on time spent on documents.

Additionally, we implemented a feature to recommend documents that users who interact with a specific document also like. The system enables filtering by document UUID and visitor ID, ensuring flexibility in analysis. We have also included error handling for missing or invalid data inputs.



##  Requirements Checklist

- Implemented in Python 3  
- Views by Country/Continent: Histograms  
- Views by Browser: Simplified & detailed histograms  
- Top Readers: Top 10 profiles based on reading time  
- “Also Likes” List & Graph: Document recommendations and visual graph  
- GUI: Tkinter-based user interface  
- CLI: Command-line testing for automation  

---

## 🛠 Design Considerations

###  File Structure

- `display_histogram.py`  
- `data_processing.py`  
- `also_likes.py`  
- `top_readers.py`  
- `cw2.py`  
- `gui.py`  
- `main.py`

###  GUI Design (Tkinter)

- Input fields for Document UUID, Visitor UUID (optional), and file path  
- Task-specific buttons  
- Graphs shown in separate windows  
- Input validation and error messaging  

###  Advanced Coding Techniques

- **Dask**: Parallel data processing for large datasets  
- **Generators**: Memory-efficient line-by-line file processing  
- **Graphviz**: Graph visualization of document relationships  

###  Usability Enhancements

- Interactive GUI for general users  
- CLI support for automated testing  
- Visual feedback, informative error messages  

---

##  User Guide

### GUI Usage

1. **Load Data**: Browse and load JSON or .gz files.  
2. **Generate Histograms**:  
   - Country / Continent views  
   - Browser usage (simplified and detailed)  
3. **Top Readers**: View top 10 readers by time spent  
4. **Also Likes**:  
   - List of similar documents  
   - Graph of relationships between documents and users  

### CLI Usage

```bash
python cw2.py -t <task_id> -f <file_name> -d <doc_uuid> -v <visitor_uuid>
