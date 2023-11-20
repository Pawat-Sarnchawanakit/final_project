from database import Database, CsvFile;
from hashlib import sha256
import secrets, json
class Role:
    Member = 0
    Lead = 1
    Faculty = 2
    Advisor = 3
    Admin = 4
    def toString(role):
        return ["Member", "Lead", "Faculty", "Advisor", "Admin"][role];

class ManageApp:
    def __init__(self):
        self.mainDatabase = Database();
        self.peopleTable = self.mainDatabase.addTable("people");
        self.peopleTable.fromCsv("ID", CsvFile("./persons.csv"));
        self.loginTable = self.mainDatabase.addTable("login");
        self.peopleTable.forEach(lambda id, entry: self.loginTable.put(f"{entry['first']}.{entry['last'][0]}", {
            "person_id": id,
            "username": f"{entry['first']}.{entry['last'][0]}",
            "password": sha256((''.join(chr(0x20) for _ in range(4)) +"42069").encode()).digest(), # + secrets.randbelow(95)
            "role": {
                "student": Role.Member,
                "faculty": Role.Faculty,
                "admin": Role.Admin,
            }[entry["type"]]
        }));
        self.projectsTable = self.mainDatabase.addTable("projects");
        self.documentsTable = self.mainDatabase.addTable("documents");
    def login(self):
        username = input("Please login\nUsername: ");
        password = sha256((input("Password: ")+"42069").encode()).digest();
        loginEntry = self.loginTable.get(username);
        if loginEntry == None:
            return;
        if loginEntry["password"] != password:
            return;
        return loginEntry;
    def adminPanel(self):
        cur = self.mainDatabase;
        curStr = '/'
        for cmd in iter(lambda: input("$ "), "exit"):
            if cmd == "ls":
                print(cur.getData());
                continue;
            if cmd == "cd":
                toCdInto = cur.get(input("Enter key: "));
                if toCdInto == None:
                    print("Entry doesn't exist.")
                    continue;
                curStr += f"{toCdInto}/";
                cur = toCdInto;
                continue;
            if cmd == "home":
                cur = self.mainDatabase;
                continue;
            if cmd == "set":
                try:
                    cur.put(input("Enter key: "), json.loads(input("Enter value: ")))
                except:
                    print("Bad value.");
                continue;
            if cmd == "get":
                entry = cur.get(input("Enter key: "))
                if entry == None:
                    print("Invalid key.")
                    continue;
                try:
                    print(json.dumps(key))
                except:
                    print(entry);
                continue;
            if cmd == "delete":
                cur.delete(input("Enter key: "))
                continue;
            if cmd == "help":
                print(
                    "ls - list all entries\n" \
                    "cd - change current table / database\n" \
                    "home - goes back to root database\n"
                    "set - set an entry\n"
                    "get - get an entry\n"
                    "delete - deletes an entry\n"
                    "help - display this"
                    )
                continue;
            print("Unknown command!\nType \"help\" for a list of commands.")
    def run(self):
        while True:
            info = self.login();
            if info == None:
                print("Invalid credentials, please try again.");
                continue;
            [lambda: None, lambda: None, lambda: None, lambda: None, self.adminPanel][info["role"]]();

ManageApp().run();
