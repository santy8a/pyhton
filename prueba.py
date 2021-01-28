import os
import sys
import shutil
import subprocess

def runCommandLdap(command): 
    output = subprocess.run(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    out = output.stdout.rstrip().decode('ascii')
    error = output.stderr.rstrip().decode('ascii')
    rc = output.returncode
    return (out,rc,error)

comando = 'ldapsearch -H ldap://10.0.0.4:3268 -x -w P@ssw0rd588588 -D "azureuser@ansible.com" "(cn=azureuser)" dn | grep dn | awk  \'{print $2}\''
terraformDeploy = runCommandLdap(comando)

print(terraformDeploy)