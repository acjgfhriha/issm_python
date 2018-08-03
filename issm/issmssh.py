from socket import gethostname
from sys import platform as _platform
import subprocess
import os
import MatlabFuncs as m

def issmssh(host,login,port,command):
	"""
	ISSMSSH - wrapper for OS independent ssh command.
 
	   usage: 
	      issmssh(host,command)
	"""

	#first get hostname 
	hostname=gethostname()

	#if same as host, just run the command. 
	if m.strcmpi(host,hostname):
		subprocess.call(command,shell=True)
	else:
		if m.ispc():
			#use the putty project plink.exe: it should be in the path.
		
			#get ISSM_DIR variable
			if 'ISSM_DIR_WIN' in os.environ:
				ISSM_DIR=os.environ['ISSM_DIR_WIN'][1:-2]
			else:
				raise OSError("issmssh error message: could not find ISSM_DIR_WIN environment variable.")

			username=raw_input('Username: (quoted string) ')
			key=raw_input('Key: (quoted string) ')

			subprocess.call('%s/externalpackages/ssh/plink.exe -ssh -l "%s" -pw "%s" %s "%s"' % (ISSM_DIR,username,key,host,command),shell=True);

		else:
			#just use standard unix ssh
			if port:
				subprocess.call('ssh -l %s -p %d localhost "%s"' % (login,port,command),shell=True)
			else:
				subprocess.call('ssh -l %s %s "%s"' % (login,host,command),shell=True)

	# The following code was added to fix:
	# "IOError: [Errno 35] Resource temporarily unavailable"
	# on the Mac when trying to display md after the solution.
	# (from http://code.google.com/p/robotframework/issues/detail?id=995)

	if _platform == "darwin":
		# Make FreeBSD use blocking I/O like other platforms
		import sys
		import fcntl
		from os import O_NONBLOCK
		
		fd = sys.stdin.fileno()
		flags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~O_NONBLOCK)
		
		fd = sys.stdout.fileno()
		flags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~O_NONBLOCK)

