import io
import os
import pickle
import csv
class CsvFile:
    def __init__(self, path):
        self.path = path;
    def read(self, callback):
        with open(self.path, "rb") as file:
            rows = csv.DictReader(file)
            for row in rows:
                callback(dict(row));

    
class Table:
    def __init__(self, dat=None):
        self.__data = {} if dat is None else dat;
    def getData(self):
        return self.__data;
    def get(self, key, default=None):
        return self.__data.get(key, default);
    def put(self, key, val):
        self.__data[key] = val;
    def delete(self, key):
        del self.__data[key];
    def fromCsv(self, key, csvFile):
        csvFile.read(lambda val: self.__data.update({val[key]: val}));
    def forEach(self, callback):
        for i, v in self.__data.items():
            callback(i, v);
    def __repr__(self):
        return f"Table{self.__data}";

class Database(Table):
    def add_table(self, name):
        newTable = Table();
        self.put(name, newTable)
        return newTable
    def load(self):
        if not os.path.exists("./database"):
            return False
        for file_name in os.listdir("./database"):
            file_path = os.path.join("./database", file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    self.put(file_name, Table(pickle.load(file)))
        return True
    def save(self):
        if not os.path.exists("./database"):
            os.makedirs("./database")
        for name, data in self.getData().items():
            with open(f"./database/{name}", "wb") as file:
                pickle.dump(data.getData(), file)
