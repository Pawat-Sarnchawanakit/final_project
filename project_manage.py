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
        self.login_table.fromCsv("username", CsvFile("./login.csv"))
        for key, val in self.login_table.getData().items():
            salt = ''.join(chr(0x20 + secrets.randbelow(95)) for _ in range(4))
            self.login_table.put(key, {
                "id": val['ID'],
                "username": val['username'],
                "password": salt + sha256((val['password'] + salt).encode()).hexdigest(),
                "role": {
                    "student": Role.Member,
                    "faculty": Role.Faculty,
                    "admin": Role.Admin,
                }[val["role"]]
            })
        self.projectsTable = self.main_database.add_table("projects")
        self.documentsTable = self.main_database.add_table("documents")
    def get_login_from_data(self, data):
        return self.login_table.get(f"{data['first']}.{data['last'][0]}")
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
    def login_prompt(self):
        info = self.login()
        if info is None:
            print("Invalid credentials, please try again.")
            return
        [
            MemberPanel, LeadPanel, lambda x,y: None,
            lambda x,y: None, AdminPanel
        ][info["role"]](self, self.people_table.get(info["id"]), info).show();
    def save(self):
        self.main_database.save();
    def run(self):
        Panel({
            'exit': ("Type `exit` to exit", False),
            'login': ("Type `login` to login", self.login_prompt)
        }).show();
        return self;
class Panel:
    def __init__(self, actions, header="What do you want to do? ", footer="Choose: "):
        self.__actions, self.__header, self.__footer = actions, header, footer;
    def show(self):
        while True:
            print(self.__header)
            for action in self.__actions.values():
                print(f"{action[0]}")
            inp = input(self.__footer)
            action_info = self.__actions.get(inp)
            if action_info is None:
                print("Invalid choice.")
                continue;
            if not action_info[1]:
                break;
            action_info[1]();

class ProjectView:
    def __init__(self, project):
        self.project = project;
    def getInfoString(self):
        return \
            f"Project Name: {self.project['name']}\n" \
            f"Project Description: {self.project['desc']}\n" \
            f"Project Id: {self.project['id']}\n" \
            f"Project Advisor: {self.project.get('advisor')}\n" \
            f"Project Leader: {self.project['members'][0]}\n" \
            f"Project Members: {self.project['members'][1:]}\n" \
            f"Approved: {'yes' if self.project.get('approved') else 'no'}\n"
    @property
    def advisor_pending(self):
        return self.project["advisor"] == "pending"
    @advisor_pending.setter
    def advisor_pending(self, new_status):
        if new_status:
            self.project["advisor"] = "pending"
            return
        self.project["advisor"] = None
        return
    @property
    def advisor_id(self):
        return self.project["advisor"]
    @advisor_id.setter
    def advisor_id(self, new_advisor_id):
        self.project["advisor"] = new_advisor_id
    @property
    def name(self):
        return self.project["name"]
    @name.setter
    def name(self, new_name):
        self.project["name"] = new_name
    @property
    def desc(self):
        return self.project["desc"]
    @desc.setter
    def desc(self, new_desc):
        self.project["desc"] = new_desc
    @property
    def approved(self):
        return self.project["approved"]
    @approved.setter
    def approved(self, new_approved):
        self.project["approved"] = new_approved
    @property
    def lead_id(self):
        return self.project["members"][0]
    @lead_id.setter
    def lead_id(self, new_lead_id):
        self.project["members"][0] = new_lead_id
    @property
    def member_ids(self):
        return self.project["members"][1::]
    @property
    def id(self):
        return self.project["id"]

class ProjectPanel:
    def __init__(self, app, project_view):
        self.app, self.project_view = app, project_view;
    def manage(self, wheel_mode):
        panel_data = {
            '1': ("1. Exit", False),
            '2': ("2. Change name", self.change_name),
            '3': ("3. Change description", self.change_desc)
        };
        if wheel_mode:
            panel_data.update({
                '4': ("4. Delete", self.proj_delete),
                '5': ("5. Invite members", self.invite_member),
                '6': ("6. Request for advisor", self.request_for_advisor),
            })
            if self.project_view.approved:
                panel_data.update({'7': ("7. Submit for evaluation", self.submit)})
        Panel(panel_data).show();
    def submit(self):
        pass
    def proj_delete(self):
        self.project_view.delete();
    def request_for_advisor(self):
        if self.project_view.advisor_pending:
            print("Please wait for the faculty you requested to either accept or reject your request before sending a new request.")
            return
        faculty_data = self.app.people_table.get(input("Enter faculty id: "))
        if faculty_data is None:
            print("Invalid faculty id.")
            return
        login_data = self.app.get_login_from_data(faculty_data);
        if login_data is None:
            print("Something went wrong, please contact an admin.")
            return
        faculty_view = FacultyView(faculty_data, login_data)
        if faculty_view.role != Role.Faculty:
            print("That person is not a faculty.")
            return
        reqs = faculty_view.requests;
        reqs.append(self.project_view.id)
        print(f"Successfully requested {faculty_view.name}")

    def invite_member(self):
        member_data = self.app.people_table.get(input("Enter member id: "))
        if member_data is None:
            print("Invalid member id.")
            return
        login_data = self.app.get_login_from_data(member_data);
        if login_data is None:
            print("Something went wrong, please contact an admin.")
            return
        member_view = MemberView(member_data, login_data)
        if member_view.role != Role.Member:
            print("That person is not a member.")
            return
        invitations = member_view.invitations;
        invitations.append(self.project_view.id)
        print(f"Successfully invited {member_view.name}")
    def change_name(self):
        self.project_view.name = input("Enter new project name: ")
        print("The project name has been changed to", self.project_view.name)
    def change_desc(self):
        self.project_view.desc = input("Enter new project description: ")
        print("The project description has been changed to: ", self.project_view.name, sep='\n')

class UserView:
    def __init__(self, user_data, login_data):
        self.user_data, self.login_data = user_data, login_data
    @property
    def name(self):
        return f"{self.user_data['first']} {self.user_data['last']}"
    @property
    def role(self):
        return self.login_data["role"]
    @property
    def id(self):
        return self.user_data["ID"]

class MessageView:
    def __init__(self, data):
        self.data = data;
    @property
    def message_type(self):
        return self.data["type"]
    @property
    def sender_id(self):
        return self.data["author"]
    def get_title(self, app: ManageApp):
        author = app.people_table.get(self.data['author'])
        if author is None:
            author = "Unknown"
        else:
            author = f"{author['first']} {author['last']}"
        return {
            "inva": f"{self.data['author']} has accepted your project {self.data['project']} invitation."
        }[self.data["type"]]


# class FacultyView(UserView):
#     def __init__(self, ):
#         self. = 

class MemberView(UserView):
    @property
    def invitations(self):
        reqs = self.user_data.get("invs", [])
        if reqs is None:
            reqs = [];
            self.user_data["invs"] = reqs;
        return reqs;
    @property
    def project_ids(self):
        projs = self.user_data.get("projs", [])
        if projs is None:
            projs = [];
            self.user_data["projs"] = projs;
        return projs;
    def become(self, role):
        self.user_data["projs"] = None;
        self.user_data["invitations"] = None;
        self.login_data["role"] = role;

class FacultyView(UserView):
    @property
    def requests(self):
        reqs = self.user_data.get("reqs", [])
        if reqs is None:
            reqs = [];
            self.user_data["reqs"] = reqs;
        return reqs;
    @property
    def project_ids(self):
        projs = self.user_data.get("projs", [])
        if projs is None:
            projs = [];
            self.user_data["projs"] = projs;
        return projs;

class FacultyPanel:
    def __init__(self, app, user_data, login_data):
        self.app, self.faculty_view = app, FacultyView(user_data, login_data);

class LeadView(MemberView):
    @property
    def messages(self):
        msgs = self.user_data.get("msgs", [])
        if msgs is None:
            msgs = [];
            self.user_data["msgs"] = msgs;
        return msgs;

class LeadPanel:
    def __init__(self, app, user_data, login_data):
        self.app, self.lead_view = app, LeadView(user_data, login_data);
    def show(self):
        Panel({
            '1': ("1. Logout", False),
            '2': ("2. View responses", self.view_responses),
            '3': ("3. View projects", self.view_projects),
            '4': ("4. Become a member", self.become_member),
        }).show();
    def become_member(self):
        self.lead_view.become(Role.Member)
        print("You've become a member.\nLogout and log back in to access member features.")
    def view_responses(self):
        msgs = self.lead_view.messages;
        if not msgs:
            print("You do not have any responses.")
            return
        idx = 0
        for msg in msgs:
            msg_view = MessageView(msg)
            print(f"{idx}. {msg_view.get_title(self.app)}")
            idx += 1;
        try:
            Panel({
                '1': ("1. Go back", False),
                '2': ("2. Delete a message", lambda: self.msg_delete(msgs, int(input("Enter an index: ")))),
                '3': ("3. Clear all messages", lambda: msgs.clear()),
            }).show();
        except:
            print("An error occurred.")
    def msg_delete(self, msgs, idx):
        msgs[idx] = msgs[-1]
        msgs.pop()
    def view_projects(self):
        projs = self.lead_view.project_ids;
        if not projs:
            print("You didn't create any projects.")
        idx = 0
        for projId in projs:
            proj = self.app.projectsTable.get(projId)
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
        cmd = input("Type `exit` to go back.\nType `create` to create a project\nType an index to manage project.\nType: ")
        if cmd == "exit":
            return;
        if cmd == "create":
            proj_view = ProjectView({
                "id": self.app.getUniqueProjectId(),
                "name": input("Enter project name: "),
                "desc": input("Enter project description: "),
                "members": [self.lead_view.id],
                "approved": False
            })
            self.app.projectsTable.put(proj_view.id, proj_view.project)
            ProjectPanel(self.app, proj_view).manage(True)
        try:
            proj_view = ProjectView(self.app.projectsTable.get(projs[int(cmd)]))
            ProjectPanel(self.app, proj_view).manage(True)
        except:
            return;
    
class MemberPanel:
    def __init__(self, app, data, loginData):
        self.app, self.member_view = app, MemberView(data, loginData);
    def show(self):
        Panel({
            '1': ("1. Logout", False),
            '2': ("2. View invitations", self.view_invitations),
            '3': ("3. Manage joined projects", self.view_joined_projects),
            '4': ("4. Become a lead", self.become_lead),
        }).show();
    def become_lead(self):
        self.member_view.become(Role.Lead);
        print("You've become a lead.\nLogout and log back in to access more features.")
    def view_joined_projects(self):
        proj_ids = self.member_view.project_ids;
        if not proj_ids:
            print("You didn't join any projects.")
            return
        idx = 0;
        for projId in proj_ids:
            proj_view = ProjectView(self.app.projectsTable.get(projId))
            print(f"=====[Project {idx}]=====\n")
            print(proj_view.getInfoString())
            idx += 1
    def view_invitations(self):
        invs = self.member_view.invitations;
        if not invs:
            print("There are no invitations at the moment.")
            return
        while True:
            print("List of invitations: ")
            idx = 0
            for req in invs:
                proj = self.app.projectsTable.get(req)
                if proj is None:
                    continue
                proj = ProjectView(proj)
                lead = self.app.people_table.get(proj.lead_id)
                if lead is None:
                    lead = "Unknown"
                else:
                    lead = f"{lead['first']} {lead['last']}"
                print(f"{idx}. {lead} invited you to join project {proj.name} ({proj.id})")
                idx += 1
            cmd = input(
                "Choose a request you want to accept, type \"exit\" to go back.\nRequest: "
            )
            if cmd == "exit":
                break
            try:
                idx = int(cmd)
                if idx >= len(invs):
                    print("Index out of bounds.")
                    continue
                projs = self.member_view.project_ids;
                projs.append(invs[idx])
                invs[idx] = invs[-1];
                invs.pop()
            except:
                pass
class AdminPanel:
    def __init__(self, app, data, loginData):
        self.data, self.loginData, self.cur, self.cur_str, self.app = data, loginData, app.main_database, '/', app;
    def show(self):
        Panel({
            'exit': ("Type `exit` to exit", False),
            'ls': ("Type `ls` to list everything under the current table.", lambda: print(self.cur.getData())),
            'cd': ("Type `cd` to go down to a specific table.", self.cd),
            'home': ("Type `home` to go back to the root database.", self.home),
            'set': ("Type `set` to set an entry in the table.", self.on_set),
            'get': ("Type `get` to get an entry in the table.", self.on_get),
            'delete': ("Type `delete` to delete an entry in the table.", lambda: self.cur.delete(input("Enter key: "))),
        }).show();
    def home(self):
        self.cur = self.app.main_database
    def cd(self):
        to_cd_into = self.cur.get(input("Enter key: "))
        if to_cd_into is None:
            print("Entry doesn't exist.")
            return
        self.cur_str += f"{to_cd_into}/"
        self.cur = to_cd_into
    def on_set(self):
        try:
            self.cur.put(input("Enter key: "),
                    json.loads(input("Enter value: ")))
        except:
            print("Bad value.")
    def on_get(self):
        entry = self.cur.get(input("Enter key: "))
        if entry is None:
            print("Invalid key.")
            return
        try:
            print(json.dumps(entry))
        except:
            print(entry)
ManageApp().run().save();
