# What's done?
 - What each role does (kinda)
# Usage
First you have to login using your username which is first name followed by a '.' and the first letter of your last name (case sensitive)  
After you login you will be directed to different menus based on your roles:  
## Admins
You can list everything by using `ls` command.  
Use `cd` to enter into different tables.  
Use `home` to return to the root database.  
Use `set` to set an entry in the table to a value, the value must be in JSON format.  
## Faculty and Advisor
For this role, you can:  
- View requests and send replies
- View projects details
- Approve project (with a token)
- Be a supervisor for a project (with a token)  

**Note: A normal faculty won't have a token. The lead will have to give the token to the faculty.**

## Lead
For this role, you can:
- Create project.
- Send request and token to others including:
  - invitations to be a member
  - approval request
  - request to be advisor
- View project details.
- Edit project info.
- View all available members (that can be useful for inviting people)  
## Member
For this role, you can:
- View messages, requests
- Accept project invitation
- View projects you have joined.
