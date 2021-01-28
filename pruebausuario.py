#!/usr/bin/env python3

from jinja2 import Template
import subprocess

data = '''
dn: CN={{common_name}},OU=cloud,DC=ansible,DC=com
objectClass: top
objectClass: group
cn: {{common_name}}
distinguishedName: CN={{common_name}},OU=cloud,DC=ansible,DC=com
name: {{common_name}}
sAMAccountName: {{common_name}}
objectCategory: CN=Group,CN=Schema,CN=Configuration,DC=ansible,DC=com
'''

tm = Template(data)
msg = tm.render(common_name='Peter')

path="/tmp/newgroups.ldif"
# f= open(path,"w+")
# f.write(msg)
# f.close

bashCommand = 'ldapadd -H ldap://10.0.0.4 -x -w P@ssw0rd588588 -D azureuser@ansible.com -f {{ path }} /tmp/newgroups.ldif'
print(bashCommand)
proc = subprocess.Popen(
    ["/usr/bin/bash", "-c", bashCommand],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)
msg = 'through stdin to stdout'.encode('utf-8')
stdout_value = proc.communicate(msg)[0].decode('utf-8')
print('pass through:', repr(stdout_value))