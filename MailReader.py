#!/usr/bin/env python
###########################
#
#  A.L.V.I. Bot
#
# MailReader.py: Handle Imap/POP connection, messages download and send vocal notification
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 12/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################





import email
import logging
import alviUtils

class MailReader:
	def __init__(self, name, server, protocol, ssl, username, password, lastid, say):
		self.name=name
		self.username=username
		self.passwd=password
		self.address = server
		self.say = say
		self.log = logging.getLogger("Alvi")
		self.lastid=str(lastid)
		self.proto=protocol
		self.ssl=ssl

	def getLastId(self):
		return self.lastid
	
	def getName(self):
		return self.name


	def read(self):
		try:
			if self.proto == 'IMAP':
				return self._readImap()
			else:
				return self._readPop()
		except:
			pass

	def _readPop():
		"""
		import poplib

		if self.ssl:
			conn = poplib.POP3_SSL(self.address)
		else:
			conn = poplib.POP3(self.address)

		pop.username(self.username)
		pop.pass_(self.passwd)
		
		numMessages=len(pop.list()[1])
		"""
		pass

	def _readImap(self):

		import imaplib

		try:
			if self.ssl:
				conn= imaplib.IMAP4_SSL(self.address)
			else:
				conn= imaplib.IMAP4(self.address)

			conn.login(self.username, self.passwd)
		except:
			message = "I am unable to connect to " +self.name
			self.log.warning(message)
			self.say(message)
			raise RuntimeError, "Cannot connect to server"
	
		code = conn.select('INBOX')[0]
	
		if code != 'OK':
			message="ERROR: Mailbox not found!!"
			self.say(message)
			self.log.warning(message)
			raise RuntimeError, "Failed to select inbox"

		code, data= conn.search(None, 'ALL')

		if code == 'OK':
			msgid_list= data[0].split()
		else:
			message="ERROR: messages DDI not found"
			self.say(message)	
			self.log.warning(message)
			raise RuntimeError, "Failed to get message IDs"


	
		if not self.lastid in msgid_list: 
			lastidx = len(msgid_list)-3
		else:
			lastidx = msgid_list.index(self.lastid)+1

		newids=msgid_list[lastidx:]
		newids.reverse()

		if len(newids) > 0: 
			self.lastid = newids[0]
			greetings="su "+self.name+"."
			self.say(greetings)

		for id in newids:
			code, data = conn.fetch(id, '(RFC822.HEADER)')

			if code == 'OK':
				mail = email.message_from_string(data[0][1])
				From_ = mail.get('From').split(' ')
				if(len(From_)>1):
					# nice-formed From. i.e.: sender <sender@mail.com>
					From = ''
					for s in From_[:-1]: From += s    # too ugly ?
					#From = From.replace('"', '')
					From = alviUtils.str_to_hlf(From)
				else:
					# old-formed From. i.e.: <sender@mail.com>
					From = alviUtils.str_to_hlf(From_[0])
			
				digest = From + " writes you: " + alviUtils.str_to_hlf(mail.get('Subject'))
				self.log.info(self.name+': '+digest)
				self.say(digest)

		
			else:
				message="ERROR: could not retrieve msg"
				self.log.warning(message)
				say(message)
				raise RuntimeError, "could not retrieve msg"
	
		conn.close()
		conn.logout()
		return self.lastid


if __name__ == "__main__":
	import config
	import festival,os

	say = festival.open().say
	
	conf = config.config(os.path.expanduser('~/.alvi.cfg'))
	conf.load()
	params = conf.getConf('Mail')
	print params
	m = MailReader(params['mail_server'],'IMAP', True, params['username'], params['password'], params['lastid'], say )
	lastid =  m.read()
	print lastid


