import os
import csv

class Map:
    def __init__(self, filename):
        self.data = {}
        self.filename = filename
        
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    key, value = row
                    self.data[key] = value
    
    def clear(self):
        self.data = {}

    def save(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            for key, value in self.data.items():
                writer.writerow([key, value])

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return ""

    def __setitem__(self, key, value):
        self.data[key] = value

