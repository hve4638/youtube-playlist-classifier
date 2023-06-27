import csv
import os

class PlaylistDB:
    header = [ "title", "channelTitle", "duration", "id", "channelId" ]

    def __init__(self):
        self.count = 0
        self.items = []
        self.idset:set = set()

    def add(self, item, ignore_duplication = False):
        if (ignore_duplication) or not (item["id"] in self.idset):
            self.idset.add(item["id"])
            self.items.append(item)

    def save(self, fname):
        with open(fname, "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writeheader()
            for item in self.items:
                writer.writerow(item)

    def load(self, fname):
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for item in reader:
                    self.add(item)

    def __iter__(self):
        return iter(self.items)

