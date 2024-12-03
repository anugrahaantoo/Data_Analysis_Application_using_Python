def analyze_top_readers(df):
    """Analyze and return the top 10 readers based on total reading time."""
    try:
        if 'visitor_uuid' not in df.columns or 'event_readtime' not in df.columns:
            print("Missing required columns: 'visitor_uuid' or 'event_readtime'")
            return []

        # Group by visitor and sum their reading time
        reader_times = df.groupby('visitor_uuid')['event_readtime'].sum()
        top_readers = reader_times.nlargest(10)

        # Format the results for display
        top_readers_list = [
            f"{uuid}: {time} seconds" for uuid, time in top_readers.items()
        ]

        return top_readers_list
    except Exception as e:
        print(f"Error analyzing top readers: {e}")
        return []