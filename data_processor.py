import json
from collections import Counter
from itertools import chain

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        with open(self.file_path, 'r') as file:
            return [json.loads(line) for line in file]

    def views_by_country(self, document_uuid):
        countries = [
            entry['visitor_country']
            for entry in self.data
            if entry['document_uuid'] == document_uuid
        ]
        return Counter(countries)

    def views_by_browser(self):
        browsers = [entry['visitor_useragent'] for entry in self.data]
        return Counter(browsers)

    def simplify_browser_names(self, browser_counter):
        simplified = Counter()
        for browser in browser_counter:
            name = browser.split('/')[0]  # Simplify to the main browser name
            simplified[name] += browser_counter[browser]
        return simplified

    def reader_profiles(self):
        reader_time = Counter()
        for entry in self.data:
            reader_time[entry['visitor_uuid']] += entry['visitor_time']
        return reader_time.most_common(10)

    def also_likes(self, document_uuid):
        readers = {entry['visitor_uuid'] for entry in self.data if entry['document_uuid'] == document_uuid}
        related_documents = Counter(
            chain.from_iterable(
                entry['document_uuid']
                for entry in self.data
                if entry['visitor_uuid'] in readers and entry['document_uuid'] != document_uuid
            )
        )
        return related_documents.most_common(10)
