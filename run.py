#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os, sys, tempfile, subprocess, shlex

################ Variables:
userad = "azureuser@ansible.com"
adserv = "10.0.0.4"
passwd = "P@ssw0rd588588"
################

cloud_provider = "GAWS"
project_name = "PLANIFAN"
project_env = "PRE"
sufix_group = "ADMINS"
ou_cloud_provider = "Amazon"
cn_group_name = cloud_provider + '-' + project_name + '-' + project_env + '-' + sufix_group

################ File to create group into AD
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('newgroups.ldif')
output = template.render(cn_group= cn_group_name, ou_provider= ou_cloud_provider)

path="/tmp/newgroups.ldif"
f= open(path,"w+")
f.write(output)
f.close()
################

# ####################### Crea GRUPO
# bashCommand = 'ldapadd -H ldap://%s -x -w %s -D %s -f %s' %(adserv, passwd, userad, path)

# proc = subprocess.Popen(
#     ["/usr/bin/bash", "-c", bashCommand],
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
# )
# # msg = 'through stdin to stdout'.encode('utf-8')
# # stdout_value = proc.communicate(msg)[0].decode('utf-8')
# # print('pass through:', repr(stdout_value))
# stdout_value = proc.communicate()[0].decode('utf-8')
# print('pass through:', repr(stdout_value))
# ####################### FIN Crea GRUPO


#ldapsearch -H ldap://10.0.0.4:3268 -x -w P@ssw0rd588588 -D "azureuser@ansible.com" "(cn=azureuser)" dn
commandUser = 'ldapsearch -H ldap://10.0.0.4:3268 -x -w P@ssw0rd588588 -D "azureuser@ansible.com" "(cn=usuario1)" dn | grep -iE "dn: cn=" | awk  \'{print $2}\''
proc = subprocess.Popen(
    ["/usr/bin/bash", "-c", commandUser],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    universal_newlines=True
)
dn_user = proc.communicate()[0]

################ File to asig user to group into AD
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('addusertogroup.ldif')
output = template.render(cn_group= cn_group_name, ou_provider= ou_cloud_provider, distinguishedNameUser= dn_user)

path="/tmp/addusertogroup.ldif"
f= open(path,"w+")
f.write(output)
f.close()

commandAddUserToGroup = 'ldapmodify -H ldap://10.0.0.4 -x -w P@ssw0rd588588 -D "azureuser@ansible.com" -f %s' %(path)
proc = subprocess.Popen(
    ["/usr/bin/bash", "-c", commandAddUserToGroup],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    universal_newlines=True
)

print(proc.communicate()[0])
