import os
import csv

class Map:
    def __init__(self, filename, newfile=False):
        self.data = {}
        self.filename = filename
        self.defGetCaller = lambda x : ""
        
        if (not newfile) and os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    key, value = row
                    self.data[key] = value

    def clear(self):
        self.data = {}

    def save(self):
        with open(self.filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for key, value in self.data.items():
                writer.writerow([key, value])

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return self.defGetCaller(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __contains__(self, value):
        return value in self.data

    def __iter__(self):
        return iter(self.data.items())