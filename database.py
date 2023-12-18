import io
import os
import pickle
import csv
class CsvFile:
    """Csv file reader class.
    """
    def __init__(self, path):
        self.path = path;
    def read(self, callback):
        """Read the csv file and calls the callback for each entry.

        Args:
            callback (function): The callback that gets called for every entry.
        """
        with open(self.path, "r", encoding="UTF-8") as file:
            rows = csv.DictReader(file)
            for row in rows:
                callback(dict(row));

    
class Table:
    """The table class containg key and value pairs.
    """
    def __init__(self, dat=None):
        self.__data = {} if dat is None else dat;
    def getData(self):
        """Gets the raw dictionary.

        Returns:
            dict: The raw dictionary.
        """
        return self.__data;
    def get(self, key, default=None):
        """Gets the value of an entry using a key.

        Args:
            key (anytype): The key.
            default (anytype, optional): The fallback value. Defaults to None.

        Returns:
            anytype: The value or else the fallback value.
        """
        return self.__data.get(key, default);
    def put(self, key, val):
        """Puts a new value in place of a key.

        Args:
            key (anytype): The key.
            val (anytype): The new value.
        """
        self.__data[key] = val;
    def delete(self, key):
        """Deletes an entry using a key.

        Args:
            key (anytype): The key.
        """
        del self.__data[key];
    def fromCsv(self, key, csvFile):
        """Read from a Csv file using the CsvFile class

        Args:
            key (str): The key of the value in the csv that is used for the table key.
            csvFile (CsvFile): The CsvFile object
        """
        csvFile.read(lambda val: self.__data.update({val[key]: val}));
    def forEach(self, callback):
        """Iterate through each entry and call a callback for each entry.

        Args:
            callback (function): The callback that gets called for each entry.
        """
        for i, v in self.__data.items():
            callback(i, v);
    def __repr__(self):
        return f"Table{self.__data}";

class Database(Table):
    def add_table(self, name):
        """Add a table to the database

        Args:
            name (str): The name of the table.

        Returns:
            Table: The newly added table.
        """
        newTable = Table();
        self.put(name, newTable)
        return newTable
    def load(self):
        """Loads data from the database directory.

        Returns:
            bool: True if succeeded else False.
        """
        if not os.path.exists("./database"):
            return False
        for file_name in os.listdir("./database"):
            file_path = os.path.join("./database", file_name)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as file:
                    self.put(file_name, Table(pickle.load(file)))
        return True
    def save(self):
        """Saves the database to the database directory.
        """
        if not os.path.exists("./database"):
            os.makedirs("./database")
        for name, data in self.getData().items():
            with open(f"./database/{name}", "wb") as file:
                pickle.dump(data.getData(), file)
