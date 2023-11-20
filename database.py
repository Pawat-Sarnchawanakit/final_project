class CsvFile:
    def __init__(self, path):
        self.path = path;
    def read(self, callback):
        import csv
        with open(self.path) as file:
            rows = csv.DictReader(file)
            for row in rows:
                callback(dict(row));

class Database(Table):
    def __init__(self, name):
        self.__name = name
    @property
    def name(self):
        return self.__name;
    def addTable(self, name):
        newTable = Table();
        self.__data[name] = newTable
        return newTable
    
class Table:
    def __init__(self):
        self.__data = {};
    def getData(self):
        return self.__data;
    def get(self, key, default=None):
        return self.__data.get(key, default);
    def put(self, key, val):
        self.__data[key] = val;
    def delete(self, key):
        del self.__data[key];
    def fromCsv(self, key, csvFile):
        csvFile.read(lambda val: self.__data.update({key: val}));
    def forEach(self, callback):
        for i, v in self.__data.items():
            callback(i, v);