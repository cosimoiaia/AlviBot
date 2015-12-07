#!/usr/bin/env python

###########################
#
#  A.L.V.I. Bot
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 12/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################


import config
import MailReader
import RssReader
import manager
import aimlBrain
import festival
import os
import logging
import readline


### Classe di appoggio per il completamento della commandLine
class Completer:
	def __init__(self, words):
		self.words = words
		self.prefix = None

	def complete(self, prefix, index):
		if prefix != self.prefix:
			self.matching_words = [w for w in self.words if w.startswith(prefix)]
			self.prefix = prefix
		try:
			return self.matching_words[index]
		except IndexError:
			return None



class Alvi:
	""" Alvi's main class """

	def loadConf(self, confFile="~/.alvi.cfg"):
		self.conf = config.config(os.path.expanduser(confFile))
		self.sched = manager.Manager()
		self.mails=[]
		self.rss=[]
		self.mboxes = []
		self.feeds = []

		# Carichiamo tutte le configurazioni
		self.conf.load()
		if self.conf.error:
			return;

		### Inizializzo il sistema di Log.
		self.log = logging.getLogger("Alvi")
		self.log.setLevel(logging.INFO)

		formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		LogHdlr = logging.FileHandler(self.conf.getConf('Log')['logfile'])
		LogHdlr.setFormatter(formatter)
		self.log.addHandler(LogHdlr)



		### Inizializzo gli oggetti relativi ai FeedRss da leggere e alle mail in base alle conf
		### e li passo allo Scheduler/Manager per essere eseguiti agli intervalli prestabiliti
		mboxes_conf= self.conf.getConf('Mail')
		feeds_conf= self.conf.getConf('Feed')

		if mboxes_conf : self.mboxes = mboxes_conf['inboxes'].split(',')
		if feeds_conf: self.feeds  = feeds_conf['rssfeeds'].split(',')

		self.log.info("Loading Mail:")
		for mbox in self.mboxes:
			self.log.info(mbox)
			cfg= self.conf.getConf(mbox.strip())
			self.log.debug(cfg)
			mail=MailReader.MailReader(mbox,cfg['mail_server'],cfg['protocol'],cfg['ssl'],cfg['username'],cfg['password'],cfg['lastid'],self.say)
			self.sched.enqueue(int(cfg['check']), mail.read)
			self.mails.append(mail)

		self.log.info("Loading Feeds:")
		for feed in self.feeds:
			cfg = self.conf.getConf(feed.strip())
			rss = RssReader.RssReader(feed, cfg['address'],cfg['check'], self.say)
			self.sched.enqueue(int(cfg['check']),rss.read)
			self.rss.append(rss)
			self.log.info(rss)


	def loadBrain(self):
		# Inizializzo la base di conoscenza aiml

		self.log.info("Carico la base di conoscenza aiml")
		self.brain = aimlBrain.AlviBrain()

	def start_tasks(self):
		self.sched.start()

	def showConf(self):
		print "[Feed Rss]"
		for feed in self.rss:
			print feed
		print "[Caselle di posta]"
		for mail in self.mails:
			print mail.getName();


	def doRssRead(self):
		for feed in self.rss:
			self.sched.immediate(feed.read)

	def doMailRead(self):
		for mail in self.mails:
			self.sched.immediate(mail.read)


	def die(self):
		self.sched.stop()		
		self.say("ahia, non vale")

		for mail in self.mails:
			self.conf.set(mail.getName(), 'lastid', mail.getLastId())	

		self.conf.save()
		self.festival.close()
	

	def help(self):
		print "Command List:"
		for cmd in self.cmdSet.keys():
			print cmd

	def loadCommandSet(self):
		### Tabella di  comandi: funzione funzione corrispondente
		self.cmdSet = { 'news': self.doRssRead, 
				'mail': self.doMailRead, 
				'showConf': self.showConf,
				'reloadBrain': self.brain.reload,
				'reloadConf': self.loadConf,
				'help': self.help 
				}

		completer = Completer(self.cmdSet.keys())
		readline.parse_and_bind("tab: complete")
		readline.set_completer(completer.complete)


	def parse_command(self, command):
	
		if self.conf.error: self.die()
	
		self.log.info("Utente: "+command)
		if command == 'quit':
			self.die()
			return False
		elif self.cmdSet.has_key(command):
			self.log.info("Alvi: eseguo "+command)
			self.cmdSet.get(command)()
		else:
			response = self.brain.answer(command)
			self.log.info("Alvi Risponde: "+response)
			self.say(response)
		return True


	def __init__(self, confFile="~/.alvi.cfg"):
		
		self.festival = festival.open()
		self.say = self.festival.say
		self.say("Sto caricando")

		
		self.loadConf(confFile)

		if self.conf.error: return

		self.loadBrain()

		self.say("Fatto. pronto e attivo")
		self.loadCommandSet()

	

if __name__ == "__main__":
	alvi = Alvi()
	try:
		import sys

		print("Alvi Bot versione 0.3.1")
		alvi.start_tasks()

		cont = True
		while cont:
			#print 'Alvi> ',
			a=raw_input('Alvi> ')
			a=a.strip()
			if not a == '': 
				cont = alvi.parse_command(a)

	except KeyboardInterrupt:
		alvi.parse_command('quit')
