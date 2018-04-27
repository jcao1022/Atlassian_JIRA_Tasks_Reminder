
from jira import JIRA
import re
import sqlite3
from email.mime.text import MIMEText
import smtplib


class JIRA_Wapper():

    def __init__(self, user, password, server_url='http://jira.calix.local', **kwargs):
        self.jira = JIRA(basic_auth=(user, password), server=server_url, **kwargs)

    def _list_projects(self):
        return sorted([pro.key for pro in self.jira.projects()])

    def _get_a_issue(self, issue_id):
        return self.jira.issue(issue_id)

    def search_issues_by_jql(self, jql, **kwargs):
        return self.jira.search_issues(jql, **kwargs)

    def get_assignee(self, issue_id):
        return self._get_a_issue(issue_id).raw['fields']['assignee']['displayName']

    def get_issue_link(self, issue_id):
        return self._get_a_issue(issue_id).raw['fields']['votes']['self'].replace('rest/api/2/issue', 'browse').replace('/votes', '')

    def get_issue_title(self, issue_id):
        return self._get_a_issue(issue_id).raw['fields']['summary']

    def get_reporter(self, issue_id):
        return self._get_a_issue(issue_id).raw['fields']['reporter']['displayName']

    def get_issue_type(self, issue_id):
        return self._get_a_issue(issue_id).raw['fields']['issuetype']['name']

    def get_priority(self, issue_id):
        return self._get_a_issue(issue_id).raw['fields']['priority']['name']

    def add_comment(self, issue_id, comment):
        self.jira.add_comment(issue_id, comment)

    def get_issue_status(self, issue_id):
        ret = self._get_a_issue(issue_id).raw['fields']['status']['name']
        return ret

    def update_issue(self, issue_id, **kwargs):
        self._get_a_issue(issue_id).update(**kwargs)

    def delete_issue(self, issue):
        issue.delete()

    def add_watcher(self, issue_id, watcher):
        self.jira.add_watcher(issue_id,watcher)

class DB_lite():
   def __init__(self):
       pass

def send_mail(data):
    # with open("prober_msg.txt", 'rb') as fp:
    #     content = fp.read()
        # content = re.sub(r"ZZZZZZ\r", data['topo'], content)
        # content = re.sub(r"XXXXXX\r", data['ip_list'], content)
    print "Sending email..."
    msg = MIMEText(data["content"])
    msg['Subject'] = data["subject"]
    msg['From'] = data['from']
    msg['To'] = data["to"]

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('mail.calix.local')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()     
    print 'Email has been sent to %s!' % data['to']

def send_mail_html(data):
    # with open("prober_msg.txt", 'rb') as fp:
    #     content = fp.read()
        # content = re.sub(r"ZZZZZZ\r", data['topo'], content)
        # content = re.sub(r"XXXXXX\r", data['ip_list'], content)
    print "Sending email..."
    msg = MIMEText(data["content"], 'html', 'utf-8')
    msg['Subject'] = data["subject"]
    msg['From'] = data['from']
    msg['To'] = data["to"]

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('mail.calix.local')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print 'Email has been sent to %s!' % data['to']


if __name__ == '__main__':

    import logo

    print logo.cafe_logo('v1','19', 20)
    # EMAIL_TITLE = raw_input('Please type your email title:')
    # JQL = raw_input('Please type your jira SQL sentence:')
    # ref_link = raw_input('Please type your reference link:')

    result = []
    jira = JIRA_Wapper('soapuser', 'Soapuser')
    # print jira.get_assignee(jira.get_a_issue('cafe-1313'))
    # print jira.get_reporter(jira.get_a_issue('cafe-1313'))
    jql1 = 'project = CAFE AND status in (Open, "In Progress", Reopened, "On Hold")'
    jql2 = 'project in (CAFE, CAFESUP, CTPT) AND status in (Open, "In Progress", Reopened, "On Hold") AND assignee in (currentUser()) ORDER BY resolution ASC'
    jql3 = 'project in (CAFE, CAFESUP, CTPT) AND status in (Open, "In Progress", Reopened, "On Hold") AND assignee in (jcao)'
    jql4 = 'project = CAFE AND Sprint in openSprints()'
    jql5 = 'project = CAFE AND Sprint in closedSprints()'
    jql6 = 'project in (CAFE, CTPT) AND assignee in (jzou)'
    jql7 = 'project = CAFE AND issuetype = Task AND status in (Open, "In Progress", Reopened, "On Hold") ORDER BY assignee'
    if not jira.search_issues_by_jql(jql7):
        import os
        print "EEROR: No issues found!"
        os._exit(0)

    for i in  jira.search_issues_by_jql(jql7):
        # print i, jira.get_reporter(i), jira.get_issue_link(i), jira.get_issue_title(i)
        result.append(
                    {'id':i.key,
                       'assignee':jira.get_assignee(i),
                       'link':jira.get_issue_link(i),
                       'issue_type':jira.get_issue_type(i),
                       'priority':jira.get_priority(i),
                       'summary':jira.get_issue_title(i),
                       'Status':jira.get_issue_status(i)
                    }
                )
    # content='ID             Repoter                      Link                                         Summary\n'
    # content='ID  Repoter  Link  Summary\n'
    content = ''
    for i in result:
        # print '#'*80
        # print '====>', i, '/*/*/*/*/*/*/*/',type(i), type(str(i['id'])), type(str(i['repoter'])), type(str(i['link'])), type(str(i['summary']))
        # content+=i['id']+'\t'+i['repoter'] + '\t\t'+i['link'] +'\t\t'+i['summary']+'\n'
        # content+=str(i['id']).ljust(10, ' ') + str(i['repoter']).ljust(10, ' ') + str(i['link']).ljust(10,' ') + str(i['summary']).ljust(10,' '), '\n'
        # print type(str(i['id']))
        # print type(str(i['repoter']))
        # print type(str(i['link']))
        # print type(str(i['summary']))
        # content += i['id'].encode('utf-8').ljust(15, ' ') + i['repoter'].encode('utf-8').ljust(29, ' ') + i['link'].encode('utf-8').ljust(45,' ') + i['summary'].encode('utf-8').ljust(60,' ')
        print type(i['assignee']), i['priority']
        content += i['id'].encode('utf-8') +"    "+ i['assignee'].encode('utf-8') + "    " + i['issue_type'].encode('utf-8') + "    " + i['Status'].encode('utf-8')+ "    " + i['priority'].encode('utf-8') + "    " + i['link'].encode('utf-8') + "    " + i['summary'].encode('utf-8')

        content += '\n'
        # content += "%s %s %s %s" % (str(i['id']).ljust(10, ' ') + str(i['repoter']).ljust(10, ' ') + str(i['link']).ljust(10, ' ') + str(i['summary']).ljust(10, ' '), '\n')
        # print '====>', content, type(content)
        # content += "%10s %20s %60s %60s +'\n'" % (i['id'], i['repoter'], i['link'], i['summary'])
    # data = {
    #     "from": "jiraBot@calix.com",
    #     "to": "james.cao@calix.com",
    #     "content": content,
    #     "subject":"Assigned to me"
    # }
    # print '#'*80
    # print content
    # print '#' * 80
    head = """
        <table width="95%" border="1">
        <tr>
        <th bgcolor="#0099cc">ID</th>
        <th bgcolor="#0099cc">Assignee</th>
        <th bgcolor="#0099cc">Issue Type</th>
        <th bgcolor="0099cc">Status</th>
        <th bgcolor="#0099cc">Priority</th>        
        <th bgcolor="#0099cc">Link</th>
        <th bgcolor="#0099cc">Summary</th>
        </tr>
        <tr>
        """
    bottom = """
        </table>
        """

    html = ""
    for i in content.splitlines():
        print i
        for x in i.split("    "):
            x=x.strip()
            if x.upper() == 'OPEN':
                html += """ <td bgcolor="#cccccc" nowrap><font color="#ff3300"> %s </td>""" % x + '\n'
            elif x.upper() == 'IN PROGRESS':
                html += """ <td bgcolor="#cccccc" nowrap><font color="#906113"> %s </td>""" % x + '\n'
            else:
                html += """ <td bgcolor="#cccccc" nowrap> %s </td> """ % x + '\n'

        html = html + '</tr>' + '\n' + '<tr>' + '\n'


    html = head + html + bottom
    # ref_link ='http://jira.calix.local/browse/CAFE-3213?filter=23858&jql=project%20%3D%20CAFE%20AND%20issuetype%20%3D%20%22Technical%20task%22%20and%20key%20%3D%20CAFE-3213'
    # html += 'Please refer to the link %s for more details.' % ref_link
    print html
    print type(html)

#     test = """
#
#     <table border="1">
#     <tr>
#     <td>row 1, cell 1</td>
#     <td>row 1, cell 2</td>
#     </tr>
#     <tr>
#     <td>row 2, cell 1</td>
#     <td>row 2, cell 2</td>
#     </tr>
#     </table>
# """

    data = {
        "from": "jiraBot@calix.com",
        "to": "automation-dev-cdc@calix.com",
        #"to": "james.cao@calix.com",
        "content": html,
        "subject": "to-do tasks"
    }

    # send_mail(data)
    send_mail_html(data)

