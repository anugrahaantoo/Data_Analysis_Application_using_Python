def top_readers(data, n=10):
    """Get the top N readers based on total time spent."""
    reader_times = data.groupby('visitor_uuid')['time_spent'].sum()
    return reader_times.nlargest(n)

def average_time_per_reader(data):
    """Calculate the average time spent by readers."""
    avg_time = data.groupby('visitor_uuid')['time_spent'].mean()
    return avg_time
