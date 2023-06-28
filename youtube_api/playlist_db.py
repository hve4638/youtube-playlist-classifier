import csv
import os

class DuplicationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'DuplicationException: {self.message}'
    
class PlaylistDB:
    header = [ "title", "channelTitle", "duration", "id", "channelId" ]

    def __init__(self):
        self.items:list = []
        self.itemsId:list = []

    def __len__(self):
        return len(self.items)

    def add(self, item, ignore_duplication = False):
        if "id" not in item:
            raise Exception(f"id not in item: {item}")
        elif (ignore_duplication) or not (item["id"] in self.itemsId):
            self.items.append(item)
            self.itemsId.append(item["id"])
        else:
            raise DuplicationException(f"{item}")
        
    def remove(self, id = None):
        index = self.itemsId.index(id)
        del self.items[index]
        del self.itemsId[index]

    def clear(self):
        self.items = []
        self.itemsId = []

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
    
    def ids(self):
        return self.itemsId[:]
    
    def __getitem__(self, id:str):
        index = self.itemsId.index(id)
        return self.items[index]


