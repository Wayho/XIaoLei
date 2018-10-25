# coding: utf-8
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot
print(chatterbot.__version__)

oChatBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

oChatBot.set_trainer(ChatterBotCorpusTrainer)
oChatBot.train("chatterbot.corpus.chinese.GBT50297")