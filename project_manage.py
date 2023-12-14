"""
The project management module.
"""
from hashlib import sha256
import secrets
import json
from database import Database, CsvFile


class Role:
    """The role enum
    """
    Member = 0
    Lead = 1
    Faculty = 2
    Advisor = 3
    Admin = 4


class ManageApp:
    """The manage app.
    """
    def __init__(self):
        self.main_database = Database()
        if self.main_database.load():
            self.people_table = self.main_database.get("people")
            self.login_table = self.main_database.get("login")
            self.projects_table = self.main_database.get("projects")
            self.documents_table = self.main_database.get("documents")
            return
        self.people_table = self.main_database.add_table("people")
        self.people_table.fromCsv("ID", CsvFile("./persons.csv"))
        self.login_table = self.main_database.add_table("login")
        self.login_table.fromCsv("username", CsvFile("./login.csv"))
        for key, val in self.login_table.getData().items():
            salt = ''.join(chr(0x20 + secrets.randbelow(95)) for _ in range(4))
            self.login_table.put(
                key, {
                    "id":
                    val['ID'],
                    "username":
                    val['username'],
                    "password":
                    salt + sha256(
                        (val['password'] + salt).encode()).hexdigest(),
                    "role": {
                        "student": Role.Member,
                        "faculty": Role.Faculty,
                        "admin": Role.Admin,
                    }[val["role"]]
                })
        self.projects_table = self.main_database.add_table("projects")
        self.documents_table = self.main_database.add_table("documents")

    def get_unique_project_id(self):
        """Generates a unique project id.

        Returns:
            str: The unique project id.
        """
        while True:
            proj_id = secrets.token_hex(16)
            if self.projects_table.get(proj_id) is None:
                return proj_id

    def get_name_from_id(self, user_id):
        """Gets a user name from their id.

        Args:
            user_id (str): The user id.

        Returns:
            str: Their full name, first name followed by last name
                or `Unknown` if the user isn't found.
        """
        name = self.people_table.get(user_id)
        if name is not None:
            return f"{name['first']} {name['last']}"
        return "Unknown"

    def get_login_from_data(self, data):
        """Retrieve the login data from user data.

        Args:
            data (dict): The user data.

        Returns:
            dict: The login data.
        """
        return self.login_table.get(f"{data['first']}.{data['last'][0]}")

    def find_user(self, username_or_id):
        """Finds a user using a username or their id.

        Args:
            username_or_id (str): Username or id.

        Returns:
            dict: The user data.
        """
        user_data = self.people_table.get(username_or_id)
        if user_data is not None:
            return user_data
        login_data = self.login_table.get(username_or_id)
        if login_data is not None:
            return self.people_table.get(login_data["id"])
        return None

    def login(self):
        """The login panel

        Returns:
            dict: The login data if succeed,
                  None if failed.
        """
        username = input("Please login\nUsername: ")
        password = input("Password: ")
        login_entry = self.login_table.get(username)
        if login_entry is None:
            return None
        password = sha256(
            (password + login_entry["password"][0:4]).encode()).hexdigest()
        if login_entry["password"][4:] != password:
            return None
        return login_entry

    def login_prompt(self):
        """The login prompts that promps the user and redirect to their panel if succeded.
        """
        info = self.login()
        if info is None:
            print("Invalid credentials, please try again.")
            return
        [MemberPanel, LeadPanel, FacultyPanel, FacultyPanel,
         AdminPanel][info["role"]](self, self.people_table.get(info["id"]),
                                   info).show()

    def save(self):
        """Saves the database into a folder called database.
        """
        self.main_database.save()

    def run(self):
        """Runs the manage app.

        Returns:
            ManageApp: The manage app.
        """
        Panel({
            'exit': ("Type `exit` to exit", False),
            'login': ("Type `login` to login", self.login_prompt)
        }).show()
        return self


class Panel:
    """Base panel
    """
    def __init__(self,
                 actions,
                 header="What do you want to do? ",
                 footer="Choose: "):
        self.__actions, self.__header, self.__footer = actions, header, footer

    def show(self):
        """Shows the panel.
        """
        while True:
            print(self.__header)
            for action in self.__actions.values():
                print(f"{action[0]}")
            inp = input(self.__footer)
            action_info = self.__actions.get(inp)
            if action_info is None:
                print("Invalid choice.")
                continue
            if not action_info[1]:
                break
            action_info[1]()


class ProjectView:
    """A wrapper class that helps deal with the data of a project.
    """
    def __init__(self, project):
        self.project = project

    def get_info_string(self, app):
        """Get the overview information of the project

        Args:
            app (ManageApp): The manage app

        Returns:
            str: The string with the overview information.
        """
        proj = self.project
        advisor = proj.get('advisor')
        if advisor is not None:
            advisor = f"{app.get_name_from_id(advisor)} ({advisor})"
        member_list = ','.join([
            f"{app.get_name_from_id(member)} ({member})"
            for member in proj['members'][1:]
        ])
        if not member_list:
            member_list = "None"
        return \
            f"Name: {proj['name']}\n" \
            f"Description: {proj['desc']}\n" \
            f"Id: {proj['id']}\n" \
            f"Advisor: {advisor}\n" \
            f"Leader: {app.get_name_from_id(proj['members'][0])} ({proj['members'][0]})\n" \
            f"Members: {member_list}\n" \
            f"Approved: {'yes' if proj.get('approved') else 'no'}\n" \
            f"Evaluated: {'yes' if self.evaluated else 'no'}\n" \
            f"Report: {proj.get('report')}"

    @property
    def advisor_pending(self):
        """Advisor pending.

        Returns:
            bool: True if the advisor is pending aka the advisor request has not been responded yet.
        """
        return self.project.get("advisor") == "pending"

    @advisor_pending.setter
    def advisor_pending(self, new_status):
        if new_status:
            self.project["advisor"] = "pending"
            return
        self.project["advisor"] = None
        return

    @property
    def advisor_id(self):
        """The advisor id.

        Returns:
            str: The advisor id, None if there's no advisor.
        """
        return self.project.get("advisor")

    @advisor_id.setter
    def advisor_id(self, new_advisor_id):
        self.project["advisor"] = new_advisor_id

    @property
    def name(self):
        """The name of the project

        Returns:
            str: The name of the project.
        """
        return self.project["name"]

    @name.setter
    def name(self, new_name):
        self.project["name"] = new_name

    @property
    def desc(self):
        """The description of the project.

        Returns:
            str: The description of the project.
        """
        return self.project["desc"]

    @desc.setter
    def desc(self, new_desc):
        self.project["desc"] = new_desc

    @property
    def approved(self):
        """Whether the project has been approved or not.

        Returns:
            bool: Whether the project has been approved or not.
        """
        return self.project.get("approved", False)

    @approved.setter
    def approved(self, new_approved):
        self.project["approved"] = new_approved

    @property
    def evaluated(self):
        """Whether the project has been evaluated or not.

        Returns:
            bool: Whether the project has been evaluated or not.
        """
        return self.project.get("evaluated", False)

    @evaluated.setter
    def evaluated(self, new_evaluated):
        self.project["evaluated"] = new_evaluated

    @property
    def lead_id(self):
        """The lead id of the project.

        Returns:
            str: The lead id of the project.
        """
        return self.project["members"][0]

    @lead_id.setter
    def lead_id(self, new_lead_id):
        self.project["members"][0] = new_lead_id

    @property
    def report(self):
        """The project's report.

        Returns:
            str: The project's report, None if there's no report.
        """
        return self.project.get("report")

    @report.setter
    def report(self, new_report):
        self.project["report"] = new_report

    @property
    def member_ids(self):
        """The ids of the member

        Returns:
            slice: The slice of the ids of the members.
        """
        return self.project["members"][1::]

    def add_member(self, new_member):
        """Adds a member to the member list

        Args:
            new_member (str): The new member id.
        """
        self.project["members"].append(new_member)

    @property
    def id(self):
        """The id of the project.

        Returns:
            str: The id of the project.
        """
        return self.project["id"]


class ProjectPanel:
    """The panel that allows you to manage a project.
    """
    def __init__(self, app, project_view):
        self.app, self.project_view = app, project_view

    def manage(self, wheel_mode):
        """Displays the panel.

        Args:
            wheel_mode (bool): Has access to more features like deleting or inviting member.
        """
        panel_data = {
            '1': ("1. Exit", False),
            '2': ("2. Change name", self.change_name),
            '3': ("3. Change description", self.change_desc)
        }
        if wheel_mode:
            panel_data.update({
                '4': ("4. Delete", self.proj_delete),
                '5': ("5. Invite members", self.invite_member),
            })
            if self.project_view.advisor_id is None:
                panel_data.update({
                    '6': ("6. Request for advisor", self.request_for_advisor)
                })
            elif not self.project_view.approved:
                panel_data.update(
                    {'6': ("6. Submit for approval", self.submit_approv)})
            elif not self.project_view.evaluated:
                panel_data.update(
                    {'6': ("6. Submit for evaluation", self.submit_eval)})
            elif self.project_view.report is None:
                panel_data.update(
                    {'6': ("6. Submit report", self.submit_report)})
        Panel(panel_data).show()

    def submit_report(self):
        """Submit a report
        """
        report = input("Please type in your report: ")
        self.project_view.report = report

    def submit_approv(self):
        """Submit an approval request.
        """
        faculty_data = self.app.people_table.get(self.project_view.advisor_id)
        if faculty_data is None:
            print("An internal error occurred.")
            return
        faculty_view = FacultyView(faculty_data, None)
        faculty_view.approval_requests.append(self.project_view.id)
        print("Succesfully sent approval request to your advisor.")

    def submit_eval(self):
        """Submit an evaluation request.
        """
        evaluation_list = self.app.documents_table.get("evaluation list")
        if evaluation_list is None:
            evaluation_list = []
            self.app.documents_table.put("evaluation list", evaluation_list)
        evaluation_list.append(self.project_view.id)
        print(
            "Succesfully put your project evaluation request up to be processed."
        )

    def proj_delete(self):
        """Deletes the project.
        """
        self.project_view.delete()
        print("Project succesfully deleted.")

    def request_for_advisor(self):
        """Requests for an advisor
        """
        if self.project_view.advisor_pending:
            print(
                "Please wait for the faculty you requested to either accept" \
                " or reject your request before sending a new request."
            )
            return
        faculty_data = self.app.find_user(input("Enter faculty id/username: "))
        if faculty_data is None:
            print("Invalid faculty id/username.")
            return
        login_data = self.app.get_login_from_data(faculty_data)
        if login_data is None:
            print("Something went wrong, please contact an admin.")
            return
        faculty_view = FacultyView(faculty_data, login_data)
        if faculty_view.role != Role.Faculty:
            print("That person is not a faculty.")
            return
        reqs = faculty_view.advisor_requests
        reqs.append(self.project_view.id)
        print(f"Successfully requested {faculty_view.name}")

    def invite_member(self):
        """Invites a member.
        """
        member_data = self.app.find_user(input("Enter member id/username: "))
        if member_data is None:
            print("Invalid member id.")
            return
        login_data = self.app.get_login_from_data(member_data)
        if login_data is None:
            print("Something went wrong, please contact an admin.")
            return
        member_view = MemberView(member_data, login_data)
        if member_view.role != Role.Member:
            print("That person is not a member.")
            return
        invitations = member_view.invitations
        invitations.append(self.project_view.id)
        print(f"Successfully invited {member_view.name}")

    def change_name(self):
        """Change the project Name
        """
        self.project_view.name = input("Enter new project name: ")
        print("The project name has been changed to", self.project_view.name)

    def change_desc(self):
        """Change the project description.
        """
        self.project_view.desc = input("Enter new project description: ")
        print("The project description has been changed to: ",
              self.project_view.name,
              sep='\n')


class UserView:
    """A wrapper class that helps deal with the data of a user.
    """
    def __init__(self, user_data, login_data):
        self.user_data, self.login_data = user_data, login_data

    @property
    def name(self):
        """The user name, first name followed by last name.

        Returns:
            str: The user name.
        """
        return f"{self.user_data['first']} {self.user_data['last']}"

    @property
    def role(self):
        """The user's role

        Returns:
            int: The user's role.
        """
        return self.login_data["role"]

    @role.setter
    def role(self, new_role):
        if not isinstance(new_role, int):
            raise TypeError
        self.login_data["role"] = new_role

    @property
    def id(self):
        """The user's id

        Returns:
            str: The user's id.
        """
        return self.user_data["ID"]


class MessageView:
    """A wrapper class that helps deal with the data of a message.
    """
    def __init__(self, data):
        self.data = data

    @property
    def message_type(self):
        """The type of the message

        Returns:
            str: The message type
        """
        return self.data["type"]

    @property
    def sender_id(self):
        """The id of the sender.

        Returns:
            str: The id of the sender.
        """
        return self.data["author"]

    def get_title(self, app: ManageApp):
        """Generates the appropriate title for the message.

        Args:
            app (ManageApp): The manage app.

        Returns:
            str: The title.
        """
        author = app.people_table.get(self.data['author'])
        if author is None:
            author = "Unknown"
        else:
            author = f"{author['first']} {author['last']}"
        project_id = self.data['project']
        project = ProjectView(app.projects_table.get(project_id, {}))
        return {
            "inva":
            f"{author} has accepted your project {project.name} ({project_id}) invitation.",
            "adva":
            f"{author} has agreed to be your project {project.name} ({project_id}) advisor.",
            "advr":
            f"{author} has rejected to be your project {project.name} ({project_id}) advisor.",
            "apra":
            f"{author} has approved your project {project.name} ({project_id}).",
            "aprr":
            f"{author} has rejected your project {project.name} ({project_id}) approval request."
        }[self.data["type"]]


class MemberView(UserView):
    """A class that makes it easier to access the raw table data of a member user.
    """
    @property
    def invitations(self):
        """The invitations.

        Returns:
            list: The list of project id of projects that invited you to join.
        """
        reqs = self.user_data.get("invs")
        if reqs is None:
            reqs = []
            self.user_data["invs"] = reqs
        return reqs

    @property
    def project_ids(self):
        """Project ids of projects you have joined.

        Returns:
            list: The list of project id of projects you have joined.
        """
        projs = self.user_data.get("projs")
        if projs is None:
            projs = []
            self.user_data["projs"] = projs
        return projs

    def become(self, role):
        """Clears current project list and invitations and set the role

        Args:
            role (int): The new role to be set to.
        """
        self.user_data["projs"] = None
        self.user_data["invitations"] = None
        self.login_data["role"] = role


class FacultyView(UserView):
    """A class that makes it easier to access the raw table data of a faculty user.
    """
    @property
    def advisor_requests(self):
        """Requests for you to be their advisor.

        Returns:
            list: The list of project ids of projects that wanted you to be their advisor.
        """
        reqs = self.user_data.get("adv_reqs")
        if reqs is None:
            reqs = []
            self.user_data["adv_reqs"] = reqs
        return reqs

    @property
    def project_ids(self):
        """The project ids of projects you are advising

        Returns:
            list: The list of project ids of projects you are advising.
        """
        projs = self.user_data.get("projs")
        if projs is None:
            projs = []
            self.user_data["projs"] = projs
        return projs

    @property
    def approval_requests(self):
        """Approval requests sent to you.

        Returns:
            list: Approval requests sent to you.
        """
        reqs = self.user_data.get("apr_reqs")
        if reqs is None:
            reqs = []
            self.user_data["apr_reqs"] = reqs
        return reqs

    @property
    def evaluating_projects(self):
        """The projects that have been assigned for you to evaluate.

        Returns:
            list: The projects that have been assigned for you to evaluate.
        """
        projs = self.user_data.get("eval_projs")
        if projs is None:
            projs = []
            self.user_data["eval_projs"] = projs
        return projs


class FacultyPanel:
    """The panel for faculty/advisor, the advisor check is inside this panel.
    """
    def __init__(self, app, user_data, login_data):
        self.app, self.faculty_view = app, FacultyView(user_data, login_data)

    def show(self):
        """Shows the faculty panel.
        """
        opts = {
            '1': ("1. Logout", False),
            '2': ("2. View advisor requests.", self.view_requests)
        }
        eval_projs = self.faculty_view.evaluating_projects
        if self.faculty_view.role == Role.Advisor:
            opts.update({
                '3': ("3. View projects", self.view_projects),
                '4':
                ("4. View project approval requests", self.view_projs_aprv)
            })
            if eval_projs:
                opts.update({
                    '5':
                    ("5. View projects awaiting evaluation", self.view_eval)
                })
        else:
            if eval_projs:
                opts.update({
                    '3':
                    ("3. View projects awaiting evaluation", self.view_eval)
                })
        Panel(opts).show()

    def view_eval(self):
        """View projects that have been assigned to you to evaluate.
        """
        reqs = self.faculty_view.evaluating_projects
        if not reqs:
            print("You do not have any projects to evaluate at the moment.")
            return
        idx = 0
        for req in reqs:
            proj = self.app.projects_table.get(req)
            if proj is None:
                print("{idx}. [DELETED PROJECT]")
                idx += 1
                continue
            proj = ProjectView(proj)
            print(f"{idx}. {proj.name} ({proj.id})")
            idx += 1
        sel = input(
            "\nSelect a request you want to deal with or type `exit` to go back.\nSelect: "
        )
        if sel == "exit":
            return
        try:
            seli = int(sel)
            req = reqs[seli]
            sel = input("Do you want to evaluate positively? (y/n) ")
            if sel in {'y', 'n'}:
                proj = self.app.projects_table.get(req)
                if proj is None:
                    print("Project is invalid.")
                    return
                proj = ProjectView(proj)
                if sel == 'y':
                    proj.evaluated = True
                reqs[seli] = reqs[-1]
                reqs.pop()
        except ValueError:
            print("Bad index")
        except IndexError:
            print("Invalid index")

    def view_projs_aprv(self):
        """Allow you to view approval requests for projects.
        """
        reqs = self.faculty_view.approval_requests
        if not reqs:
            print("You do not have any requests at the moment.")
            return
        idx = 0
        for req in reqs:
            proj = self.app.projects_table.get(req)
            if proj is None:
                print("{idx}. Unknown wanted you to approve [DELETED PROJECT]")
                idx += 1
                continue
            proj = ProjectView(proj)
            author = self.app.people_table.get(proj.lead_id)
            if author is None:
                author = "Unknown"
            else:
                author = f"{author['first']} {author['last']}"
            print(
                f"{idx}. {author} wanted you to approve project {proj.name} ({proj.id})"
            )
            idx += 1
        sel = input(
            "\nSelect a request you want to deal with or type `exit` to go back.\nSelect: "
        )
        if sel == "exit":
            return
        try:
            seli = int(sel)
            req = reqs[seli]
            sel = input("Do you want to approve? (y/n) ")
            if sel in {'y', 'n'}:
                proj = self.app.projects_table.get(req)
                if proj is None:
                    print("Project is invalid.")
                    return
                proj = ProjectView(proj)
                if sel == 'y':
                    proj.approved = True
                lead_data = self.app.people_table.get(proj.lead_id)
                lead_view = LeadView(lead_data, None)
                lead_view.messages.append({
                    "type": "apra" if sel == 'y' else "aprr",
                    "author": self.faculty_view.id,
                    "project": proj.id
                })
                reqs[seli] = reqs[-1]
                reqs.pop()
        except ValueError:
            print("Bad index")
        except IndexError:
            print("Invalid index")

    def view_requests(self):
        """Allows you to view and manage requests.
        """
        reqs = self.faculty_view.advisor_requests
        if not reqs:
            print("You do not have any requests at the moment.")
            return
        idx = 0
        for req in reqs:
            proj = self.app.projects_table.get(req)
            if proj is None:
                print(
                    "{idx}. Unknown invited you to be an advisor for [DELETED PROJECT]"
                )
                idx += 1
                continue
            proj = ProjectView(proj)
            author = self.app.people_table.get(proj.lead_id)
            if author is None:
                author = "Unknown"
            else:
                author = f"{author['first']} {author['last']}"
            print(
                f"{idx}. {author} invited you to be an advisor for project {proj.name} ({proj.id})"
            )
            idx += 1
        sel = input(
            "\nSelect a request you want to deal with or type `exit` to go back.\nSelect: "
        )
        if sel == "exit":
            return
        try:
            seli = int(sel)
            req = reqs[seli]
            sel = input("Do you want to accept the request? (y/n) ")
            if sel in {'y', 'n'}:
                proj = self.app.projects_table.get(req)
                if proj is None:
                    print("Project is invalid.")
                    return
                proj = ProjectView(proj)
                if sel == 'y':
                    proj.advisor_id = self.faculty_view.id
                    self.faculty_view.project_ids.append(req)
                    if self.faculty_view.role != Role.Advisor:
                        print(
                            "You've become an advisor, please logout and" \
                            " log back in to gain access to more features."
                        )
                    self.faculty_view.role = Role.Advisor
                else:
                    proj.advisor_id = None
                lead_data = self.app.people_table.get(proj.lead_id)
                lead_view = LeadView(lead_data, None)
                lead_view.messages.append({
                    "type": "adva" if sel == 'y' else "advr",
                    "author": self.faculty_view.id,
                    "project": proj.id
                })
                reqs[seli] = reqs[-1]
                reqs.pop()
        except ValueError:
            print("Bad index")
        except IndexError:
            print("Invalid index")

    def view_projects(self):
        """View the projects that the advisor is advising.
        """
        projs = self.faculty_view.project_ids
        if not projs:
            print("You aren't advising any projects.")
        idx = 0
        for proj_id in projs:
            proj = self.app.projects_table.get(proj_id)
            print(f"=====[Project {idx}]=====\n{proj.get}")
            idx += 1


class LeadView(MemberView):
    """A class that makes it easier to access the raw table data of a lead user.
    """
    @property
    def messages(self):
        """The list messages.

        Returns:
            list: The list of messages.
        """
        msgs = self.user_data.get("msgs")
        if msgs is None:
            msgs = []
            self.user_data["msgs"] = msgs
        return msgs


class LeadPanel:
    """The panel for Lead to manage things.
    """
    def __init__(self, app, user_data, login_data):
        self.app, self.lead_view = app, LeadView(user_data, login_data)

    def show(self):
        """Shows the panel.
        """
        Panel({
            '1': ("1. Logout", False),
            '2': ("2. View responses", self.view_responses),
            '3': ("3. View projects", self.view_projects),
            '4': ("4. Become a member", self.become_member),
        }).show()

    def become_member(self):
        """Make the current lead become a member.
        """
        self.lead_view.become(Role.Member)
        print(
            "You've become a member.\nLogout and log back in to access member features."
        )

    def view_responses(self):
        """View reposeses to requests, invitations, etc
        """
        msgs = self.lead_view.messages
        if not msgs:
            print("You do not have any responses.")
            return
        idx = 0
        for msg in msgs:
            msg_view = MessageView(msg)
            print(f"{idx}. {msg_view.get_title(self.app)}")
            idx += 1
        try:
            Panel({
                '1': ("1. Go back", False),
                '2':
                ("2. Delete a message",
                 lambda: self.msg_delete(msgs, int(input("Enter an index: ")))
                 ),
                '3': ("3. Clear all messages", msgs.clear),
            }).show()
        except ValueError:
            print("Bad index")

    def msg_delete(self, msgs, idx):
        """Deletes a message from a list of messages in O(1)

        Args:
            msgs (list): The messages
            idx (int): The index of the message to delete.
        """
        msgs[idx] = msgs[-1]
        msgs.pop()

    def view_projects(self):
        """Displays the list of projects and allow you to manage it.
        """
        projs = self.lead_view.project_ids
        if not projs:
            print("You didn't create any projects.")
        idx = 0
        for proj_id in projs:
            proj = self.app.projects_table.get(proj_id)
            if proj is not None:
                print(
                    f"=====[Project {idx}]=====\n{ProjectView(proj).get_info_string(self.app)}"
                )
            idx += 1
        cmd = input(
            "Type `exit` to go back.\nType `create` to create a project\n" \
                "Type an index to manage project.\nType: "
        )
        if cmd == "exit":
            return
        if cmd == "create":
            proj_view = ProjectView({
                "id":
                self.app.get_unique_project_id(),
                "name":
                input("Enter project name: "),
                "desc":
                input("Enter project description: "),
                "members": [self.lead_view.id],
                "approved":
                False
            })
            self.app.projects_table.put(proj_view.id, proj_view.project)
            self.lead_view.project_ids.append(proj_view.id)
            ProjectPanel(self.app, proj_view).manage(True)
            return
        try:
            proj_view = ProjectView(self.app.projects_table.get(projs[int(cmd)]))
            ProjectPanel(self.app, proj_view).manage(True)
        except (ValueError, IndexError):
            print("Bad index")


class MemberPanel:
    """A panel that allows members to manage things.
    """
    def __init__(self, app, data, login_data):
        self.app, self.member_view = app, MemberView(data, login_data)

    def show(self):
        """Show the member panel
        """
        Panel({
            '1': ("1. Logout", False),
            '2': ("2. View invitations", self.view_invitations),
            '3': ("3. Manage joined projects", self.view_joined_projects),
            '4': ("4. Become a lead", self.become_lead),
        }).show()

    def become_lead(self):
        """Become a lead.
        """
        self.member_view.become(Role.Lead)
        print(
            "You've become a lead.\nLogout and log back in to access more features."
        )

    def view_joined_projects(self):
        """View projects you have joined.
        """
        proj_ids = self.member_view.project_ids
        if not proj_ids:
            print("You didn't join any projects.")
            return
        idx = 0
        for proj_id in proj_ids:
            proj_view = ProjectView(self.app.projects_table.get(proj_id))
            print(f"=====[Project {idx}]=====")
            print(proj_view.get_info_string(self.app))
            idx += 1

    def view_invitations(self):
        """View invitations to join a project.
        """
        invs = self.member_view.invitations
        if not invs:
            print("There are no invitations at the moment.")
            return
        while True:
            print("List of invitations: ")
            idx = 0
            for req in invs:
                proj = self.app.projects_table.get(req)
                if proj is None:
                    continue
                proj = ProjectView(proj)
                lead = self.app.people_table.get(proj.lead_id)
                if lead is None:
                    lead = "Unknown"
                else:
                    lead = f"{lead['first']} {lead['last']}"
                print(
                    f"{idx}. {lead} invited you to join project {proj.name} ({proj.id})"
                )
                idx += 1
            cmd = input(
                "Choose a request you want to deal with, type \"exit\" to go back.\nRequest: "
            )
            if cmd == "exit":
                break
            try:
                idx = int(cmd)
                if idx >= len(invs):
                    print("Index out of bounds.")
                    continue
                if input("Do you want to accept? (y/n) ") == 'y':
                    projs = self.member_view.project_ids
                    projs.append(invs[idx])
                    proj = self.app.projects_table.get(invs[idx])
                    if proj is not None:
                        proj = ProjectView(proj)
                        proj.add_member(self.member_view.id)
                invs[idx] = invs[-1]
                invs.pop()
            except ValueError:
                pass


class AdminPanel:
    """The panel for Admin to manage things.
    """
    def __init__(self, app, data, login_data):
        self.data, self.login_data, self.cur, self.cur_str, self.app = \
            data, login_data, app.main_database, '/', app

    def show(self):
        """Shows the admin panel
        """
        Panel({
            'exit': ("Type `exit` to exit", False),
            'ls': ("Type `ls` to list everything under the current table.",
                   lambda: print(self.cur.getData())),
            'cd': ("Type `cd` to go down to a specific table.", self.cd),
            'home':
            ("Type `home` to go back to the root database.", self.home),
            'set': ("Type `set` to set an entry in the table.", self.on_set),
            'get': ("Type `get` to get an entry in the table.", self.on_get),
            'delete': ("Type `delete` to delete an entry in the table.",
                       lambda: self.cur.delete(input("Enter key: "))),
            'assign': ("Type `assign` to assign an evaluator for a project.",
                       self.assign_eval)
        }).show()

    def assign_eval(self):
        """Assign a project evaluation task to a faculty.
        """
        evaluation_list = self.app.documents_table.get("evaluation list")
        if evaluation_list is None:
            evaluation_list = []
            self.app.documents_table.put("evaluation list", evaluation_list)
        idx = 0
        for project_id in evaluation_list:
            project = self.app.projects_table.get(project_id)
            if project is None:
                idx += 1
                continue
            project = ProjectView(project)
            print(f"=====[Project {idx}]=====")
            print(project.get_info_string(self.app))
            idx += 1
        project_idx = None
        try:
            project_idx = int(input("Please enter a project index: "))
        except ValueError:
            print("Invalid index")
            return
        if project_idx < 0 or project_idx >= len(evaluation_list):
            print("Invalid index")
            return
        project = self.app.projects_table.get(evaluation_list[project_idx])
        if project is None:
            print("Invalid project")
        project = ProjectView(project)
        evaluator = self.app.find_user(
            input("Please enter username/id of the evaluator: "))
        if evaluator is None:
            print("Invalid evaluator: ")
            return
        evaluator = FacultyView(evaluator,
                                self.app.get_login_from_data(evaluator))
        if evaluator.role not in {Role.Advisor, Role.Faculty}:
            print("The evaluator must be a faculty.")
            return
        evaluator.evaluating_projects.append(project.id)
        print(f"Succesfully set the evaluator to be {evaluator.name}")

    def home(self):
        """Go back to root.
        """
        self.cur = self.app.main_database

    def cd(self):
        """Goes into a sub table
        """
        to_cd_into = self.cur.get(input("Enter key: "))
        if to_cd_into is None:
            print("Entry doesn't exist.")
            return
        self.cur_str += f"{to_cd_into}/"
        self.cur = to_cd_into

    def on_set(self):
        """Set a value of a key.
        """
        try:
            self.cur.put(input("Enter key: "),
                         json.loads(input("Enter value: ")))
        except json.decoder.JSONDecodeError:
            print("Bad value.")

    def on_get(self):
        """Get a value from a key
        """
        entry = self.cur.get(input("Enter key: "))
        if entry is None:
            print("Invalid key.")
            return
        try:
            print(json.dumps(entry))
        except TypeError:
            print(entry)


ManageApp().run().save()
