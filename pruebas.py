import subprocess

print('popen2:')

bashCommand = 'ldapadd -H ldap://10.0.0.4 -x -w P@ssw0rd588588 -D azureuser@ansible.com -f /tmp/newgroups.ldif'
proc = subprocess.Popen(
    ["/usr/bin/bash", "-c", bashCommand],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)
msg = 'through stdin to stdout'.encode('utf-8')
stdout_value = proc.communicate(msg)[0].decode('utf-8')
print('pass through:', repr(stdout_value))