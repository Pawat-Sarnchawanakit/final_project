from hashlib import sha256
import secrets
import json
from database import Database, CsvFile

class Role:
    Member = 0
    Lead = 1
    Faculty = 2
    Advisor = 3
    Admin = 4


class ManageApp:

    def __init__(self):
        self.main_database = Database()
        if self.main_database.load():
            self.people_table = self.main_database.get("people")
            self.login_table = self.main_database.get("login")
            self.projectsTable = self.main_database.get("projects")
            self.documentsTable = self.main_database.get("documents")
            return
        self.people_table = self.main_database.add_table("people")
        self.people_table.fromCsv("ID", CsvFile("./persons.csv"))
        self.login_table = self.main_database.add_table("login")
        self.people_table.forEach(lambda id, entry: self.login_table.put(
            f"{entry['first']}.{entry['last'][0]}",
            {
                "person_id":
                id,
                "username":
                f"{entry['first']}.{entry['last'][0]}",
                "password": (lambda passwd, salt: salt + sha256(
                    (passwd + salt).encode()).hexdigest())
                (''.join(chr(0x20 + secrets.randbelow(95)) for _ in range(4)), ''.join(
                    chr(0x20 + secrets.randbelow(95))
                    for _ in range(4))),
                "role": {
                    "student": Role.Member,
                    "faculty": Role.Faculty,
                    "admin": Role.Admin,
                }[entry["type"]]
            }))
        self.projectsTable = self.main_database.add_table("projects")
        self.documentsTable = self.main_database.add_table("documents")

    def login(self):
        username = input("Please login\nUsername: ")
        password = input("Password: ")
        loginEntry = self.login_table.get(username)
        if loginEntry is None:
            return
        password = sha256(
            (password + loginEntry["password"][0:4]).encode()).hexdigest()
        if loginEntry["password"][4:] != password:
            return
        return loginEntry

    def admin_panel(self, _=None):
        cur = self.main_database
        curStr = '/'
        for cmd in iter(lambda: input("$ "), "exit"):
            if cmd == "ls":
                print(cur.getData())
                continue
            if cmd == "cd":
                toCdInto = cur.get(input("Enter key: "))
                if toCdInto is None:
                    print("Entry doesn't exist.")
                    continue
                curStr += f"{toCdInto}/"
                cur = toCdInto
                continue
            if cmd == "home":
                cur = self.main_database
                continue
            if cmd == "set":
                try:
                    cur.put(input("Enter key: "),
                            json.loads(input("Enter value: ")))
                except:
                    print("Bad value.")
                continue
            if cmd == "get":
                entry = cur.get(input("Enter key: "))
                if entry is None:
                    print("Invalid key.")
                    continue
                try:
                    print(json.dumps(entry))
                except:
                    print(entry)
                continue
            if cmd == "delete":
                cur.delete(input("Enter key: "))
                continue
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
                continue
            print("Unknown command!\nType \"help\" for a list of commands.")

    def send_msg(self, data, target_id):
        targetData = self.people_table.get(target_id)
        reqs = targetData.get("requests")
        if reqs is None:
            reqs = []
            targetData["requests"] = reqs
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
        for cmd in iter(
                lambda: input("0. Go back\n"
                              "1. Reply\n"
                              "2. Reply and delete\n"
                              "3. Delete\nChoose: "), "0"):
            if cmd == '1':
                self.send_msg(data, req['sender']['id'])
                continue
            if cmd == '2':
                self.send_msg(data, req['sender']['id'])
                return True
                continue
            if cmd == '3':
                return True

    def requests_panel(self, data):
        reqs = data.get("requests", [])
        while True:
            if not reqs:
                print("There are no requests at the moment.")
                return
            print("List of requests: ")
            idx = 0
            for req in reqs:
                print(f"{idx}. {req['title']} - {req['sender']['name']}")
                idx += 1
            cmd = input(
                "Choose a request you want to view, type \"exit\" to exit.\nRequest: "
            )
            if cmd == "exit":
                break
            try:
                idx = int(cmd)
                if idx >= len(reqs):
                    print("Index out of bounds.")
                    continue
                if self.requestPanel(data, req):
                    reqs[idx] = reqs[::-1][0]
                    reqs.pop()
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
                items = self.projectsTable.getData().items()
                if not items:
                    print("There are no projects.")
                    continue
                for i, v in items:
                    print(i, v)
                continue
            if cmd == '2':
                project = self.projectsTable.get(input("Enter project id: "))
                if project is None:
                    print("Invalid project id.")
                    continue
                curAdvisor = project["advisor"]
                if curAdvisor is not None and input(
                    "There is already an advisor for this project.\n" \
                    "Do you want to overwrite this? (y/n) "
                    ) != 'y':
                    continue
                if sha256(proj["secret"] + "ADV" +
                          data["ID"]).hexdigest()[0:5] != input(
                              "Enter token: "):
                    print("Invalid token.")
                    continue
                curAdvisor = {
                    "name": f"{data['first']} {data['last']}",
                    "id": data["ID"]
                }
                project["advisor"] = curAdvisor
                continue
            if cmd == '3':
                project = self.projectsTable.get(input("Enter project id: "))
                if project is None:
                    print("Invalid project id.")
                    continue
                if sha256(proj["secret"] + "APR" +
                          data["ID"]).hexdigest()[0:5] != input(
                              "Enter token: "):
                    print("Invalid token.")
                    continue
                project["approved"] = True
            if cmd == '4':
                project = self.projectsTable.get(input("Enter project id: "))
                if project is None:
                    print("Invalid project id.")
                    continue
                print(project)

    def facultyPanel(self, data):
        for cmd in iter(lambda: input(
            "What do you want to do?\n" \
            "0. Exit\n" \
            "1. View requests to be a supervisor\n" \
            "2. View projects\n\nChoose: " \
            ), '0'):
            if cmd == '1':
                self.requests_panel(data)
                continue
            if cmd == '2':
                self.allProjectsPanel(data)
                continue

    def getUniqueProjectId(self):
        while True:
            id = secrets.token_hex(16)
            if self.projectsTable.get(id) is None:
                return id

    def manageProjectPanel(self, data, proj):
        for inp in iter(lambda: input(
            "What do you want to do?\n" \
            "0. Go back\n" \
            "1. Edit name\n" \
            "2. Edit description\n" \
            "3. Invite member\n" \
            "4. Request for advisor\n" \
            "5. Submit report\n\nChoose: " \
            ), '0'):
            if inp == '0':
                break;
            if inp == '1':
                proj["name"] = input("Enter new name: ")
                continue
            if inp == '2':
                proj["desc"] = input("Enter new description: ")
                continue
            if inp in {'3', '4'}:
                nameOrId = input("Enter target username or id: ")
                tarData = self.people_table.get(nameOrId)
                if tarData is None:
                    tarLoginData = self.login_table.get(nameOrId)
                    if tarLoginData is None:
                        print("Invalid username or id.")
                        continue
                    tarData = self.people_table.get(tarLoginData["person_id"])
                target_id = tarData["ID"]
                token = sha256(proj["secret"] + {
                    '3': "INV",
                    '4': "ADV"
                }[inp] + target_id).hexdigest()[0:5]
                print(
                    f"The token has been generated: {token}\n"
                    "Do not forget to include this in your request!"
                )
                self.send_msg(data, target_id)
                continue
            if inp == '5':
                advisor = proj.get("advisor")
                if advisor is None:
                    print("You don't have an advisor.")
                    continue
                proj["report"] = input("Enter report: ")
                token = sha256(proj["secret"] + "APR" +
                               target_id).hexdigest()[0:5]
                targetData = self.people_table.get(advisor["id"])
                reqs = targetData.get("requests")
                if reqs is None:
                    reqs = []
                    targetData["requests"] = reqs
                reqs.append({
                    "title":
                    f"Request for project approval for {proj['name']} {proj['id']}",
                    "content": f"Token is {token}",
                    "sender": {
                        "name": f"{data['first']} {data['last']}",
                        "id": data["ID"]
                    }
                })
                continue

    def leadPanel(self, data):
        for cmd in iter(lambda: input(
            "What do you want to do?\n" \
            "0. Exit\n" \
            "1. Create a project\n" \
            "2. View all available members\n" \
            "3. Send Message\n" \
            "4. View personal projects\n\nChoose: " \
            ), '0'):
            if cmd == '1':
                projs = data.get("projects")
                if projs is None:
                    projs = []
                    data["projects"] = projs
                projId = self.getUniqueProjectId()
                newProj = {
                    "name":
                    input("Enter project name: "),
                    "desc":
                    input("Enter description: "),
                    "id":
                    projId,
                    "secret":
                    secrets.token_hex(16),
                    "members": [{
                        "name": f"{data['first']} {data['last']}",
                        "id": data['ID']
                    }]
                }
                projs.append(newProj)
                continue
            if cmd == '2':
                for v in self.login_table.getData().values():
                    if v["role"] != Role.Member:
                        continue
                    print(v["username"], v["person_id"])
                continue
            if cmd == '3':
                self.send_msg(data, input("Enter target id: "))
                continue
            if cmd == '4':
                projs = data.get("projects")
                if projs is None:
                    print("You dont have any projects.")
                    continue
                while True:
                    idx = 0
                    for proj in projs:
                        print(
                            f"=====[Project {idx}]=====\n" \
                            f"Project Name: {proj['name']}\n" \
                            f"Project Description: {proj['desc']}\n" \
                            f"Project Id: {proj['id']}\n" \
                            f"Project Advisor: {proj.get('advisor')}\n"
                            f"Project Leader: {proj['members'][0]}\n"
                            f"Project Members: {proj['members'][1:]}\n"
                            f"Approved: {'yes' if proj.get('approved') else 'no'}\n"
                        )
                        idx += 1
                    inp = input("0. Go back\n"
                                "1. Manage project\n"
                                "What do you want to do? ")
                    if inp == '0':
                        break
                    if inp == '1':
                        selProj = None
                        try:
                            curIdx = int(input("Project index: "))
                            selProj = projs[curIdx]
                        except:
                            print("Invalid index")
                            continue
                        self.manageProjectPanel(data, selProj)
                        selProj["name"] = input("New name: ")
                        continue
                continue

    def memberPanel(self, data):
        for cmd in iter(lambda: input(
            "What do you want to do?\n" \
            "0. Exit\n" \
            "1. View messages\n" \
            "2. Accept project invitation\n" \
            "3. View personal projects\n" \
            "4. Become a lead\n\nChoose: " \
            ), '0'):
            if cmd == '1':
                self.requests_panel(data)
                continue
            if cmd == '2':
                projId = input("Enter project id: ")
                proj = self.projectsTable.get(projId)
                if proj is None:
                    print("Invalid project id.")
                    continue
                if sha256(proj["secret"] + "INV" +
                          data["ID"]).hexdigest()[0:5] != input(
                              "Enter token: "):
                    print("Invalid token.")
                    continue
                projs = data.get("projects")
                if projs is None:
                    projs = []
                    data["projects"] = projs
                projs.append(proj)
                continue
            if cmd == '3':
                projs = data.get("projects")
                if projs is None:
                    print("You didn't join any projects.")
                    continue
                idx = 0
                for proj in projs:
                    print(
                        f"=====[Project {idx}]=====\n" \
                        f"Project Name: {proj['name']}\n" \
                        f"Project Description: {proj['desc']}\n" \
                        f"Project Id: {proj['id']}\n" \
                        f"Project Advisor: {proj.get('advisor')}\n"
                        f"Project Leader: {proj['members'][0]}\n"
                        f"Project Members: {proj['members'][1:]}\n"
                        f"Approved: {'yes' if proj.get('approved') else 'no'}\n"
                    )
                    idx += 1
                continue
            if cmd == '4':
                data["requests"] = None;
                loginTab = self.login_table.get(f"{data['first']}.{data['last'][0]}")
                loginTab["role"] = Role.Lead
                self.leadPanel(data);
                break;
    def save(self):
        self.main_database.save();
    def run(self):
        while True:
            if input("Type exit to `exit`, type `login` to login.\n>") == "exit":
                break;
            info = self.login()
            if info is None:
                print("Invalid credentials, please try again.")
                continue
            [
                self.memberPanel, self.leadPanel, self.facultyPanel,
                self.facultyPanel, self.admin_panel
            ][info["role"]](self.people_table.get(info["person_id"]))
        return self;

ManageApp().run().save();
