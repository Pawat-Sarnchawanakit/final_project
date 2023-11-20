from database import Database, CsvFile;
from hashlib import sha256
mainDatabase = Database() \
                    .addTable("people") \
                    .addTable("login") \
                    .addTable("projects") \
                    .addTable("documents");
mainDatabase.get("people").fromCsv(CsvFile("./persons.csv"));

# Initalize login table
def initLoginTable():
    loginTable = mainDatabase.get("login");
    mainDatabase.get("people").forEach(lambda entry: loginTable.set(entry.));
class Person:
    def __init__(self):
        pass
class LoginEntry:
    def __init__(self, person_id, password, role):
        self.person_id, self.password, self.role = person_id, password, role;

class Roles:
    Member = 0
    Lead = 1
    Faculty = 2
    Advisor = 3
    Admin = 4
    def toString(role):
        return ["Member", "Lead", "Faculty", "Advisor", "Admin"][role];

database.CsvReader("./persons.csv").read(Person, lambda personData: peopleDatabase.put(personData.ID, personData));
# peopleDatabase.forEach(lambda id, person: loginDatabase.put(f"{person.fist}.{person.last}", LoginEntry(id, sha256((abw+"42069").encode()).digest(), {'admin': Roles.Admin, 'student': Roles.Member, 'faculty': Roles.Faculty}[person.type])))

while True:
    username = input("Please login ;)\nUsername: ")
    password = sha256((input("Password: ")+"42069").encode()).digest()
    entry = loginDatabase.get(username);
    if entry == None or entry.password != password:
        print("Invalid credentials!\nAnd no one has valid credentials cuz only admins can add login table.\nHowever admins can't even login cuz the login table is literally empty.")
        continue;
    #entry.password
# start by adding the admin related code

# create an object to read an input csv file, persons.csv

# create a 'persons' table

# add the 'persons' table into the database

# create a 'login' table

# the 'login' table has the following keys (attributes):

# person_id
# username
# password
# role

# a person_id is the same as that in the 'persons' table
# let a username be a person's fisrt name followed by a dot and the first letter of that person's last name
# let a password be a random four digits string
# let the initial role of all the students be Member
# let the initial role of all the faculties be Faculty

# you create a login table by performing a series of insert operations; each insert adds a dictionary to a list

# add the 'login' table into the database

# add code that performs a login task; asking a user for a username and password; returning [person_id, role] if valid, otherwise returning None
