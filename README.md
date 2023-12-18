
# Usage
- Run the `project_manage.py` file using the python interpreter:   
```
$ python project_manage.py
What do you want to do? 
Type `exit` to exit
Type `login` to login
Choose:
```
- Login
```
Choose: login
Please login
Username: Lionel.M
Password: 2977 
What do you want to do?
1. Logout
2. View invitations
3. Manage joined projects
4. Become a lead
Choose:
```
- Do whatever you want to do, E.g. create a project
```
Choose: 4
You've become a lead.
Logout and log back in to access more features.
What do you want to do?
1. Logout
2. View invitations
3. Manage joined projects
4. Become a lead
Choose: 1
What do you want to do?
Type `exit` to exit
Type `login` to login
Choose: login
Please login
Username: Lionel.M
Password: 2977 
What do you want to do?
1. Logout
2. View responses
3. View projects
4. Become a member
Choose: 3
You didn't create any projects.
Type `exit` to go back.
Type `create` to create a project
Type an index to manage project.
Type: create
Enter project name: Automatic Recycle Bin
Enter project description: A Recycle Bin that automatically recycles stuff inside it.
What do you want to do?
1. Exit
2. Change name
3. Change description
4. Delete
5. Invite members
6. Request for advisor
Choose: 1
What do you want to do?
1. Logout
2. View responses
3. View projects
4. Become a member
Choose: 1
What do you want to do? 
Type `exit` to exit
Type `login` to login
Choose: exit
```
# Bugs
Check issues.

# Table
|Role|Action|Method|Class|Progress
-|-|-|-|-|
Admin|ls|lambda|AdminPanel|100%
Admin|cd|cd|AdminPanel|100%
Admin|home|home|AdminPanel|100%
Admin|set|on_set|AdminPanel|100%
Admin|get|on_get|AdminPanel|100%
Admin|delete|lambda|AdminPanel|100%
Admin|assign|assign_eval|AdminPanel|100%
Member|View invitations|view_invitations|MemberPanel|100%
Member|Manage joined projects|view_joined_projects|MemberPanel|100%
Member|Become Lead|become_lead|MemberPanel|100%
Lead|View responses (to requests and invitations)|view_responses|LeadPanel|100%
Lead|View Projects|view_projects|LeadPanel|100%
Lead|Become Member|become_member|LeadPanel|100%
Faculty and Advisor|View advisor requests|view_requests|FacultyPanel|100%
Faculty and Advisor|View projects awaiting evaluation|view_eval|FacultyPanel|100%
Advisor|View projects|view_projects|FacultyPanel|100%
Advisor|View project approval requests|view_projs_aprv|FacultyPanel|100%


<a id="database"></a>

# database.py

<a id="database.CsvFile"></a>

## CsvFile Class

```python
class CsvFile()
```

Csv file reader class.

<a id="database.CsvFile.read"></a>

#### read

```python
def read(callback)
```

Read the csv file and calls the callback for each entry.

Args:
    callback (function): The callback that gets called for every entry.

<a id="database.Table"></a>

## Table Class

```python
class Table()
```

The table class containg key and value pairs.

<a id="database.Table.getData"></a>

#### getData

```python
def getData()
```

Gets the raw dictionary.

Returns:
    dict: The raw dictionary.

<a id="database.Table.get"></a>

#### get

```python
def get(key, default=None)
```

Gets the value of an entry using a key.

Args:
    key (anytype): The key.
    default (anytype, optional): The fallback value. Defaults to None.

Returns:
    anytype: The value or else the fallback value.

<a id="database.Table.put"></a>

#### put

```python
def put(key, val)
```

Puts a new value in place of a key.

Args:
    key (anytype): The key.
    val (anytype): The new value.

<a id="database.Table.delete"></a>

#### delete

```python
def delete(key)
```

Deletes an entry using a key.

Args:
    key (anytype): The key.

<a id="database.Table.fromCsv"></a>

#### fromCsv

```python
def fromCsv(key, csvFile)
```

Read from a Csv file using the CsvFile class

Args:
    key (str): The key of the value in the csv that is used for the table key.
    csvFile (CsvFile): The CsvFile object

<a id="database.Table.forEach"></a>

#### forEach

```python
def forEach(callback)
```

Iterate through each entry and call a callback for each entry.

Args:
    callback (function): The callback that gets called for each entry.

<a id="database.Database"></a>

## Database Class

```python
class Database(Table)
```

<a id="database.Database.add_table"></a>

#### add\_table

```python
def add_table(name)
```

Add a table to the database

Args:
    name (str): The name of the table.

Returns:
    Table: The newly added table.

<a id="database.Database.load"></a>

#### load

```python
def load()
```

Loads data from the database directory.

Returns:
    bool: True if succeeded else False.

<a id="database.Database.save"></a>

#### save

```python
def save()
```

Saves the database to the database directory.


# test.py
The test file used for testing the project.  

<a id="project_manage"></a>

# project\_manage.py

The project management module.

<a id="project_manage.Role"></a>

## Role Class

```python
class Role()
```

The role enum

<a id="project_manage.ManageApp"></a>

## ManageApp Class

```python
class ManageApp()
```

The manage app.

<a id="project_manage.ManageApp.get_unique_project_id"></a>

#### get\_unique\_project\_id

```python
def get_unique_project_id()
```

Generates a unique project id.

Returns:
    str: The unique project id.

<a id="project_manage.ManageApp.get_name_from_id"></a>

#### get\_name\_from\_id

```python
def get_name_from_id(user_id)
```

Gets a user name from their id.

Args:
    user_id (str): The user id.

Returns:
    str: Their full name, first name followed by last name
        or `Unknown` if the user isn't found.

<a id="project_manage.ManageApp.get_login_from_data"></a>

#### get\_login\_from\_data

```python
def get_login_from_data(data)
```

Retrieve the login data from user data.

Args:
    data (dict): The user data.

Returns:
    dict: The login data.

<a id="project_manage.ManageApp.find_user"></a>

#### find\_user

```python
def find_user(username_or_id)
```

Finds a user using a username or their id.

Args:
    username_or_id (str): Username or id.

Returns:
    dict: The user data.

<a id="project_manage.ManageApp.login"></a>

#### login

```python
def login()
```

The login panel

Returns:
    dict: The login data if succeed,
          None if failed.

<a id="project_manage.ManageApp.login_prompt"></a>

#### login\_prompt

```python
def login_prompt()
```

The login prompts that promps the user and redirect to their panel if succeded.

<a id="project_manage.ManageApp.save"></a>

#### save

```python
def save()
```

Saves the database into a folder called database.

<a id="project_manage.ManageApp.run"></a>

#### run

```python
def run()
```

Runs the manage app.

Returns:
    ManageApp: The manage app.

<a id="project_manage.Panel"></a>

## Panel Class

```python
class Panel()
```

Base panel

<a id="project_manage.Panel.show"></a>

#### show

```python
def show()
```

Shows the panel.

<a id="project_manage.ProjectView"></a>

## ProjectView Class

```python
class ProjectView()
```

A wrapper class that helps deal with the data of a project.

<a id="project_manage.ProjectView.get_info_string"></a>

#### get\_info\_string

```python
def get_info_string(app)
```

Get the overview information of the project

Args:
    app (ManageApp): The manage app

Returns:
    str: The string with the overview information.

<a id="project_manage.ProjectView.advisor_pending"></a>

#### advisor\_pending

```python
@property
def advisor_pending()
```

Advisor pending.

Returns:
    bool: True if the advisor is pending aka the advisor request has not been responded yet.

<a id="project_manage.ProjectView.advisor_id"></a>

#### advisor\_id

```python
@property
def advisor_id()
```

The advisor id.

Returns:
    str: The advisor id, None if there's no advisor.

<a id="project_manage.ProjectView.name"></a>

#### name

```python
@property
def name()
```

The name of the project

Returns:
    str: The name of the project.

<a id="project_manage.ProjectView.desc"></a>

#### desc

```python
@property
def desc()
```

The description of the project.

Returns:
    str: The description of the project.

<a id="project_manage.ProjectView.approved"></a>

#### approved

```python
@property
def approved()
```

Whether the project has been approved or not.

Returns:
    bool: Whether the project has been approved or not.

<a id="project_manage.ProjectView.evaluated"></a>

#### evaluated

```python
@property
def evaluated()
```

Whether the project has been evaluated or not.

Returns:
    bool: Whether the project has been evaluated or not.

<a id="project_manage.ProjectView.lead_id"></a>

#### lead\_id

```python
@property
def lead_id()
```

The lead id of the project.

Returns:
    str: The lead id of the project.

<a id="project_manage.ProjectView.report"></a>

#### report

```python
@property
def report()
```

The project's report.

Returns:
    str: The project's report, None if there's no report.

<a id="project_manage.ProjectView.member_ids"></a>

#### member\_ids

```python
@property
def member_ids()
```

The ids of the member

Returns:
    slice: The slice of the ids of the members.

<a id="project_manage.ProjectView.add_member"></a>

#### add\_member

```python
def add_member(new_member)
```

Adds a member to the member list

Args:
    new_member (str): The new member id.

<a id="project_manage.ProjectView.id"></a>

#### id

```python
@property
def id()
```

The id of the project.

Returns:
    str: The id of the project.

<a id="project_manage.ProjectPanel"></a>

## ProjectPanel Class

```python
class ProjectPanel()
```

The panel that allows you to manage a project.

<a id="project_manage.ProjectPanel.manage"></a>

#### manage

```python
def manage(wheel_mode)
```

Displays the panel.

Args:
    wheel_mode (bool): Has access to more features like deleting or inviting member.

<a id="project_manage.ProjectPanel.submit_report"></a>

#### submit\_report

```python
def submit_report()
```

Submit a report

<a id="project_manage.ProjectPanel.submit_approv"></a>

#### submit\_approv

```python
def submit_approv()
```

Submit an approval request.

<a id="project_manage.ProjectPanel.submit_eval"></a>

#### submit\_eval

```python
def submit_eval()
```

Submit an evaluation request.

<a id="project_manage.ProjectPanel.proj_delete"></a>

#### proj\_delete

```python
def proj_delete()
```

Deletes the project.

<a id="project_manage.ProjectPanel.request_for_advisor"></a>

#### request\_for\_advisor

```python
def request_for_advisor()
```

Requests for an advisor

<a id="project_manage.ProjectPanel.invite_member"></a>

#### invite\_member

```python
def invite_member()
```

Invites a member.

<a id="project_manage.ProjectPanel.change_name"></a>

#### change\_name

```python
def change_name()
```

Change the project Name

<a id="project_manage.ProjectPanel.change_desc"></a>

#### change\_desc

```python
def change_desc()
```

Change the project description.

<a id="project_manage.UserView"></a>

## UserView Class

```python
class UserView()
```

A wrapper class that helps deal with the data of a user.

<a id="project_manage.UserView.name"></a>

#### name

```python
@property
def name()
```

The user name, first name followed by last name.

Returns:
    str: The user name.

<a id="project_manage.UserView.role"></a>

#### role

```python
@property
def role()
```

The user's role

Returns:
    int: The user's role.

<a id="project_manage.UserView.id"></a>

#### id

```python
@property
def id()
```

The user's id

Returns:
    str: The user's id.

<a id="project_manage.MessageView"></a>

## MessageView Class

```python
class MessageView()
```

A wrapper class that helps deal with the data of a message.

<a id="project_manage.MessageView.message_type"></a>

#### message\_type

```python
@property
def message_type()
```

The type of the message

Returns:
    str: The message type

<a id="project_manage.MessageView.sender_id"></a>

#### sender\_id

```python
@property
def sender_id()
```

The id of the sender.

Returns:
    str: The id of the sender.

<a id="project_manage.MessageView.get_title"></a>

#### get\_title

```python
def get_title(app: ManageApp)
```

Generates the appropriate title for the message.

Args:
    app (ManageApp): The manage app.

Returns:
    str: The title.

<a id="project_manage.MemberView"></a>

## MemberView Class

```python
class MemberView(UserView)
```

A class that makes it easier to access the raw table data of a member user.

<a id="project_manage.MemberView.invitations"></a>

#### invitations

```python
@property
def invitations()
```

The invitations.

Returns:
    list: The list of project id of projects that invited you to join.

<a id="project_manage.MemberView.project_ids"></a>

#### project\_ids

```python
@property
def project_ids()
```

Project ids of projects you have joined.

Returns:
    list: The list of project id of projects you have joined.

<a id="project_manage.MemberView.become"></a>

#### become

```python
def become(role)
```

Clears current project list and invitations and set the role

Args:
    role (int): The new role to be set to.

<a id="project_manage.FacultyView"></a>

## FacultyView Class

```python
class FacultyView(UserView)
```

A class that makes it easier to access the raw table data of a faculty user.

<a id="project_manage.FacultyView.advisor_requests"></a>

#### advisor\_requests

```python
@property
def advisor_requests()
```

Requests for you to be their advisor.

Returns:
    list: The list of project ids of projects that wanted you to be their advisor.

<a id="project_manage.FacultyView.project_ids"></a>

#### project\_ids

```python
@property
def project_ids()
```

The project ids of projects you are advising

Returns:
    list: The list of project ids of projects you are advising.

<a id="project_manage.FacultyView.approval_requests"></a>

#### approval\_requests

```python
@property
def approval_requests()
```

Approval requests sent to you.

Returns:
    list: Approval requests sent to you.

<a id="project_manage.FacultyView.evaluating_projects"></a>

#### evaluating\_projects

```python
@property
def evaluating_projects()
```

The projects that have been assigned for you to evaluate.

Returns:
    list: The projects that have been assigned for you to evaluate.

<a id="project_manage.FacultyPanel"></a>

## FacultyPanel Class

```python
class FacultyPanel()
```

The panel for faculty/advisor, the advisor check is inside this panel.

<a id="project_manage.FacultyPanel.show"></a>

#### show

```python
def show()
```

Shows the faculty panel.

<a id="project_manage.FacultyPanel.view_eval"></a>

#### view\_eval

```python
def view_eval()
```

View projects that have been assigned to you to evaluate.

<a id="project_manage.FacultyPanel.view_projs_aprv"></a>

#### view\_projs\_aprv

```python
def view_projs_aprv()
```

Allow you to view approval requests for projects.

<a id="project_manage.FacultyPanel.view_requests"></a>

#### view\_requests

```python
def view_requests()
```

Allows you to view and manage requests.

<a id="project_manage.FacultyPanel.view_projects"></a>

#### view\_projects

```python
def view_projects()
```

View the projects that the advisor is advising.

<a id="project_manage.LeadView"></a>

## LeadView Class

```python
class LeadView(MemberView)
```

A class that makes it easier to access the raw table data of a lead user.

<a id="project_manage.LeadView.messages"></a>

#### messages

```python
@property
def messages()
```

The list messages.

Returns:
    list: The list of messages.

<a id="project_manage.LeadPanel"></a>

## LeadPanel Class

```python
class LeadPanel()
```

The panel for Lead to manage things.

<a id="project_manage.LeadPanel.show"></a>

#### show

```python
def show()
```

Shows the panel.

<a id="project_manage.LeadPanel.become_member"></a>

#### become\_member

```python
def become_member()
```

Make the current lead become a member.

<a id="project_manage.LeadPanel.view_responses"></a>

#### view\_responses

```python
def view_responses()
```

View reposeses to requests, invitations, etc

<a id="project_manage.LeadPanel.msg_delete"></a>

#### msg\_delete

```python
def msg_delete(msgs, idx)
```

Deletes a message from a list of messages in O(1)

Args:
    msgs (list): The messages
    idx (int): The index of the message to delete.

<a id="project_manage.LeadPanel.view_projects"></a>

#### view\_projects

```python
def view_projects()
```

Displays the list of projects and allow you to manage it.

<a id="project_manage.MemberPanel"></a>

## MemberPanel Class

```python
class MemberPanel()
```

A panel that allows members to manage things.

<a id="project_manage.MemberPanel.show"></a>

#### show

```python
def show()
```

Show the member panel

<a id="project_manage.MemberPanel.become_lead"></a>

#### become\_lead

```python
def become_lead()
```

Become a lead.

<a id="project_manage.MemberPanel.view_joined_projects"></a>

#### view\_joined\_projects

```python
def view_joined_projects()
```

View projects you have joined.

<a id="project_manage.MemberPanel.view_invitations"></a>

#### view\_invitations

```python
def view_invitations()
```

View invitations to join a project.

<a id="project_manage.AdminPanel"></a>

## AdminPanel Class

```python
class AdminPanel()
```

The panel for Admin to manage things.

<a id="project_manage.AdminPanel.show"></a>

#### show

```python
def show()
```

Shows the admin panel

<a id="project_manage.AdminPanel.assign_eval"></a>

#### assign\_eval

```python
def assign_eval()
```

Assign a project evaluation task to a faculty.

<a id="project_manage.AdminPanel.home"></a>

#### home

```python
def home()
```

Go back to root.

<a id="project_manage.AdminPanel.cd"></a>

#### cd

```python
def cd()
```

Goes into a sub table

<a id="project_manage.AdminPanel.on_set"></a>

#### on\_set

```python
def on_set()
```

Set a value of a key.

<a id="project_manage.AdminPanel.on_get"></a>

#### on\_get

```python
def on_get()
```

Get a value from a key

