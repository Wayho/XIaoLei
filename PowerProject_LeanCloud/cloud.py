# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError

import subprocess
import select
import requests
import time
import random
import os
import codecs
import psutil

from praseword import Prase_File

engine = Engine()

APP_ROOT = os.environ.get('LEANCLOUD_APP_REPO_PATH')
APP_DOMAIN = os.environ.get('LEANCLOUD_APP_DOMAIN')

print 'APP_ROOT:',APP_ROOT
print 'APP_DOMAIN:',APP_DOMAIN

########## Base Functions ##################
def Save_To_File(filename,text):
	ffile = codecs.open( filename, 'w', 'utf-8')
	ffile.write(text)
	ffile.close()

def Load_From_File(filename):
	ffile = codecs.open( filename, 'r', 'utf-8')
	text = ffile.read()
	ffile.close()
	return text

###############################################

@engine.define( 'prasefile' )
def prasefile():
	Prase_File()
	return True

@engine.define( 'ls' )
def cmd_ls():
	OutputShell('ls -l')
	return True

@engine.define( 'top' )
def cmd_top():
	OutputShell('top -b -n 1 -H')
	return True

@engine.define( 'ps' )
def cmd_ps():
	OutputShell('ps -eLf')
	return True

@engine.define( 'cpuinfo' )
def cmd_cpuinfo():
	OutputShell('cat /etc/issue && cat /proc/cpuinfo')
	return True

@engine.define( 'shell' )
# 调试 {'cmd':'ls -l' }
def OutputShell( cmd, **params ):
	print 'shell:',cmd
	result = subprocess.Popen(
		#[ "ping 127.0.0.1" ],
		#[ "find /usr" ],
		[ cmd ],
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	)
	# read date from pipe
	select_rfds = [ result.stdout, result.stderr ]
	while len( select_rfds ) > 0:
		(rfds, wfds, efds) = select.select( select_rfds, [ ], [ ] ) #select函数阻塞进程，直到select_rfds中的套接字被触发
		if result.stdout in rfds:
			readbuf_msg = result.stdout.readline()      #行缓冲
			if len( readbuf_msg ) == 0:
				select_rfds.remove( result.stdout )     #result.stdout需要remove，否则进程不会结束
			else:
				print readbuf_msg,

		if result.stderr in rfds:
			readbuf_errmsg = result.stderr.readline()
			if len( readbuf_errmsg ) == 0:
				select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
			else:
				print readbuf_errmsg,
	result.wait() # 等待字进程结束( 等待shell命令结束 )
	#print result.returncode
	##(stdoutMsg,stderrMsg) = result .communicate()#非阻塞时读法.
	return result.returncode