#!/usr/bin/env python

###########################
#
#  A.L.V.I. Bot
#
#  config.py: Usefull class to retrive config from file. 
#
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 12/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################




import ConfigParser,os



class config:
	def __init__(self, configfile):
		self.config_file=configfile
		self.config = ConfigParser.SafeConfigParser()
		self.error=False


	def load(self):
		try:
			self.config.readfp(open(self.config_file))
		except:
			print "Attenzione, non ho trovato nessuna configurazione! Controlla per favore"
			self.error=True

	def save(self):
		try:
			with open(self.config_file, 'wb') as configfd: self.config.write(configfd)
		except:
			print "Errore, non riesco a salvere il file di configurazione!!!"

	def set(self, section, option, value):
		try:
			self.config.set(section,option,value)
		except:
			print "Errore, sezione non esistente o tipo sbagliato di opzione"

	def getConf(self, section):
		if self.config.has_section(section):
			confdict = dict(self.config.items(section))
			return confdict
		else:
			print "sezione " + section + " non esistente"
			return []

	def error(self):
		return self.error




if __name__ == "__main__":
	conf = config(os.path.expanduser('alvi.cfg'))
	conf.load()
	mboxes=conf.getConf('Mail')['inboxes'].split(',')
	mboxes_conf = []
	for m in mboxes:
		print m
		mboxes_conf += [conf.getConf(m.strip())]
	feeds=conf.getConf('Feed')['rssfeeds'].split(',')
	feeds_conf = []
	
	for f in feeds:
		print f
		feeds_conf += [conf.getConf(f.strip())]

	print mboxes_conf
	print feeds_conf
	
	
