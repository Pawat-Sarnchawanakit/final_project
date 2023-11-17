# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv

def readCsv(path, objType, callback):
    with open(path) as f:
        rows = csv.DictReader(f)
        for r in rows:
            obj = objType()
            for i, v in r.items():
                setattr(obj, i, v);
            callback(obj);



# add in code for a Database class
class Database:
    def __init__(self):
        self.data = {};
    def get(self, key, default=None):
        return self.data.get(key, default);
    def put(self, key, val):
        self.data[key] = val;
    def forEach(self, callback):
        for i, v in self.data.items():
            callback(i, v);
# add in code for a Table class

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary
