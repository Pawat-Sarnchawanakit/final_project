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
            "password": (lambda passwd, salt: salt + sha256((passwd+salt).encode()).hexdigest())(''.join(chr(0x20) for _ in range(4)), ''.join(chr(0x20 + secrets.randbelow(95)) for _ in range(4))), # + secrets.randbelow(95)
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
        password = input("Password: ");
        loginEntry = self.loginTable.get(username);
        if loginEntry == None:
            return;
        password = sha256((password+loginEntry["password"][0:4]).encode()).hexdigest();
        if loginEntry["password"][4:] != password:
            return;
        return loginEntry;
    def adminPanel(self,_=None):
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
                    print(json.dumps(entry))
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
    def sendMsg(self, data, targetId):
        targetData = self.peopleTable.get(targetId)
        reqs = targetData.get("requests");
        if reqs == None:
            reqs = [];
            targetData["requests"] = reqs;
        reqs.append({
            "title": input("Enter title: "),
            "content": input("Enter message: "),
            "sender": {
                "name": f"{data['first']} {data['last']}",
                "id": data["ID"]
            }
        })
    def requestPanel(self, data, req):
        print(f"Title: {req['title']}\n\n{req['content']}")
        for cmd in iter(lambda: input(
            "0. Go back\n"
            "1. Reply\n"
            "2. Reply and delete\n"
            "3. Delete\nChoose: "), "0"):
            if cmd == '1':
                self.sendMsg(data, req['sender']['id'])
                continue;
            if cmd == '2':
                self.sendMsg(data, req['sender']['id'])
                return True;
                continue;
            if cmd == '3':
                return True;
    def requestsPanel(self, data):
        reqs = data.get("requests", []);
        while True:
            if not reqs:
                print("There are no requests at the moment.")
                return;
            print("List of requests: ")
            idx = 0;
            for req in reqs:
                print(f"{idx}. {req['title']} - {req['sender']['name']}");
                idx += 1;
            cmd = input("Choose a request you want to view, type \"exit\" to exit.\nRequest: ");
            if cmd == "exit":
                break;
            try:
                idx = int(cmd);
                if idx >= len(reqs):
                    print("Index out of bounds.")
                    continue;
                if self.requestPanel(data, req):
                    reqs[idx] = reqs[::-1][0];
                    reqs.pop();
            except:
                pass
    def allProjectsPanel(self, data):
        for cmd in iter(lambda: input(
            "What do you want to do?\n" \
            "0. Go back\n" \
            "1. View all projects\n" \
            "2. Be an advisor for a project\n" \
            "3. Approve a project\n" \
            "4. View project info\n\nChoose: " \
            ), '0'):
            if cmd == '1':
                items = self.projectsTable.getData().items();
                if not items:
                    print("There are no projects.")
                    continue;
                for i, v in items:
                    print(i, v);
                continue;
            if cmd == '2':
                project = self.projectsTable.get(input("Enter project id: "))
                if project == None:
                    print("Invalid project id.")
                    continue;
                curAdvisor = project["advisor"];
                if curAdvisor != None and input(
                    "There is already an advisor for this project.\n" \
                    "Do you want to overwrite this? (y/n) "
                    ) != 'y':
                    continue;
                curAdvisor = {
                    "name": f"{data['first']} {data['last']}",
                    "id": data["ID"]
                };
                project["advisor"] = curAdvisor;
                continue;
            if cmd == '3':
                project = self.projectsTable.get(input("Enter project id: "))
                if project == None:
                    print("Invalid project id.")
                    continue;
                project["approved"] = True;
            if cmd == '4':
                project = self.projectsTable.get(input("Enter project id: "))
                if project == None:
                    print("Invalid project id.")
                    continue;
                print(project)
    def facultyPanel(self, data):
        for cmd in iter(lambda: input(
            "What do you want to do?\n" \
            "0. Exit\n" \
            "1. View requests to be a supervisor\n" \
            "2. View projects\n\nChoose: " \
            ), '0'):
            if cmd == '1':
                self.requestsPanel(data);
                continue;
            if cmd == '2':
                self.allProjectsPanel(data);
                continue;
    def run(self):
        while True:
            info = self.login();
            if info == None:
                print("Invalid credentials, please try again.");
                continue;
            [lambda: None, lambda: None, self.facultyPanel, self.facultyPanel, self.adminPanel][info["role"]](self.peopleTable.get(info["person_id"]));

ManageApp().run();
