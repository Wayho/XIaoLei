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

engine = Engine()
from classmingyan import MINGYAN_CLASS
from wechatclient import send_random_message,send_random_message_to_all
from juzimi import Class_Http_Get_Writer, Class_Http_Get_MingYan

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
#How to use in miniapp of wechat
#var paramsJson = {
#        paramsJson: {
#            pr_string: "ls -l",
#            pr_int: 123,
#            pr_date: Date.now(),
#            pr_pointer:'5b5b42b4808ca4006fc6e1e4',
#            pr_json:{
#                pr_string: "type string",
#                pr_int: 456,
#                pr_date: Date.now(),
#            }
#        }
#    };
#    AV.Cloud.run('test', paramsJson).then(console.log('call cloudfun test ok'))
###############################################
#半小时运行一次
# 15 5/15 9-23 * * ?
APP_DOMAIN = os.environ.get('LEANCLOUD_APP_DOMAIN')     #domain
@engine.define( 'heart' )
def Heart(**params):
	response = requests.get( "http://" + APP_DOMAIN + ".leanapp.cn/heart" )
	print ('..Heart End')
	return True

@engine.define( 'prase' )
def cmd_prase():
	#juzimi = Class_Http_Get_Writer()
	#juzimi.Http_Get_Writer_Url()

	MingYan = Class_Http_Get_MingYan()
	#MingYan.Http_Get_MinYan()
	MingYan.Test()
	#MingYan.Http_Get_MinJu_All()

	#juzimi.Test()
	return True

#@engine.define( 'import' )
def cmd_import():
	MINGYAN_CLASS.Import()
	return True

@engine.define( 'randomall' )
def cmd_random_all():
	send_random_message_to_all()
	send_random_message_to_all()
	send_random_message_to_all()

@engine.define( 'random' )
def cmd_random():
	print (send_random_message('oZtJK1HT5ueWXBeX4wMu1ze2Sm98'))

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
	print( 'shell:',cmd)
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
				print( readbuf_msg)

		if result.stderr in rfds:
			readbuf_errmsg = result.stderr.readline()
			if len( readbuf_errmsg ) == 0:
				select_rfds.remove( result.stderr )     #result.stderr，否则进程不会结束
			else:
				print(readbuf_msg)
	result.wait() # 等待字进程结束( 等待shell命令结束 )
	#print result.returncode
	##(stdoutMsg,stderrMsg) = result .communicate()#非阻塞时读法.
	return result.returncode

