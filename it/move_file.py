import os
from shutil import copyfile
import shutil
import smb
import smbclient
from django.http import HttpResponse
import json

import tempfile
from smb.SMBConnection import SMBConnection
import os
import paramiko 

def share_server(request):	
	#smb://172.16.5.100/finance/
	# ssh = paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# ssh.connect('172.16.5.100', username="munish", password="mt#684*321")
	# sftp = ssh.open_sftp()
	# localpath = 'abc.txt'
	# remotepath = '/opt/crestelsetup/patchzip'
	# sftp.put(localpath, remotepath)
	# sftp.close()
	# ssh.close()
	return HttpResponse(json.dumps('done'))