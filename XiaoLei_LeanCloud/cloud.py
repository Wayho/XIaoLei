# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError


from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot
print(chatterbot.__version__)

engine = Engine()

oChatBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

#oChatBot.set_trainer(ChatterBotCorpusTrainer)
#oChatBot.train("chatterbot.corpus.chinese.GBT50297")


@engine.define
def hello(**params):
	if 'name' in params:
		return 'Hello, {}!'.format(params['name'])
	else:
		return 'Hello, LeanCloud!'


###############################################
@engine.define( 'chat' )
def chat(sString):
	return msg(sString)

###############################################
def msg(sUserText):
	sRet = oChatBot.get_response(sUserText)
	print(sUserText, sRet)
	return str(sRet)