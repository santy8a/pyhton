import os
import sys
import shutil
import subprocess
import time

from jinja2 import Environment, FileSystemLoader

def getTimeStamp():
    ts = time.gmtime()
    filename = time.strftime("%Y%m%d%s", ts)
    return (filename)

def writeFile(filePath,text):
    f= open(filePath,"w+")
    f.write(text)
    f.close()

def createTemplate(pathTemplate,templaeName,render):
    file_loader = FileSystemLoader(pathTemplate)
    env = Environment(loader=file_loader)
    template = env.get_template(templaeName)
    output = template.render(render)
    return (output)

def runCommandV2(command):
    proc = subprocess.Popen(
        ["/usr/bin/bash", "-c", command],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    out = proc.communicate()[0]
    return (out)

def getMask(argument): 
    switcher = { 
        32: "27", 
        64: "26", 
        128: "25",
        256: "24",
    } 
    return switcher.get(argument, "nothing")

### Variables
userad = "azureuser@ansible.com"
adserv = "10.0.0.4"
passwd = "P@ssw0rd588588"
userinfoblox = "sanale"
passinfoblox = "Mapfre.1234"
hostinfoblox = "10.230.93.16"
globalnetwork = "10.85.0.0/17"
reservmask = getMask(32)
pathFileCreateGroups = "/tmp/newgroups" +getTimeStamp() +".ldif"
pathFileAddUsers = "/tmp/addusers" +getTimeStamp() +".ldif"
###

### Commands
commandCreateGroup = 'ldapadd -H ldap://%s -x -w %s -D %s -f %s' %(adserv, passwd, userad, pathFileCreateGroups)
commandSearchUser = 'ldapsearch -H ldap://%s:3268 -x -w %s -D %s "(cn=usuario1)" dn | grep -iE "dn: cn=" | awk  \'{print $2}\'' %(adserv, passwd, userad)
commandAddUserToGroup = 'ldapmodify -H ldap://%s -x -w %s -D %s -f %s' %(adserv, passwd, userad, pathFileAddUsers)
commandReservIP = """
curl -k -u %s:%s -X POST 'https://%s/wapi/v2.9.1/network?_return_fields=network,comment&_return_as_object=1' -H 'content-type: application/json' -d '{"network":"func:nextavailablenetwork:%s,MAPFRE_GLOBAL,%s","network_view":"MAPFRE_GLOBAL","comment":"AWSIBM"}' | grep '"network": ' | awk '{print $2}' | tr -d '"'
""" %(userinfoblox, passinfoblox, hostinfoblox, globalnetwork, reservmask)
###

renderCreateGroup = {
  "cn_group"    : "grupo1",
  "ou_provider" : "Amazon"
}
templateCreateGroup = createTemplate('templates','newgroups.ldif',renderCreateGroup)
writeFile(pathFileCreateGroups,templateCreateGroup)
print(runCommandV2(commandCreateGroup))

dnUser = runCommandV2(commandSearchUser)
renderAddUser = {
  "cn_group"              : "grupo1", 
  "ou_provider"           : "Amazon", 
  "distinguishedNameUser" : dnUser
}
templateAddUser = createTemplate('templates','addusertogroup.ldif',renderAddUser)
writeFile(pathFileAddUsers,templateAddUser)
print(runCommandV2(commandAddUserToGroup))

print(commandReservIP)
