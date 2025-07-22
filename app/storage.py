
import threading
from datetime import datetime

class InMemoryStore:
    def __init__(self):
        self.url_map = {}  # short_code -> full URL
        self.stats = {}    # short_code -> {clicks, created_at}
        self.lock = threading.Lock()

    def save(self, short_code, full_url):
        with self.lock:
            self.url_map[short_code] = full_url
            self.stats[short_code] = {
                'clicks': 0,
                'created_at': datetime.utcnow()
            }

    def get_url(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.stats:
                self.stats[short_code]['clicks'] += 1

    def get_stats(self, short_code):
        with self.lock:
            return self.stats.get(short_code)

store = InMemoryStore()
