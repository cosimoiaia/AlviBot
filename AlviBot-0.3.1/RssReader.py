#!/usr/bin/env python
###########################
#
#  A.L.V.I. Bot
#
# RssReader.py: Handle FeedRss reading. Check and validate URL, download digest and read last news
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 21/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################

import string
import feedparser
import logging
import formencode.validators as validator
import alviUtils


class RssReader:
	def __init__(self,name, address, check, say):
		url= address.replace('\"', '')
		self.say=say
		self.name=name
		self.log = logging.getLogger("Alvi")
		self.check = int(check) * 60
		self.oldNews = []

		#check if Rss exists
		try:
			urlValidator=validator.URL(check_exists=True)
			self.address = urlValidator.to_python(url)
		except validator.Invalid:
			self.address="none"

	def read(self):
		if self.address == "none":
			message= self.name + " non ha un indirizzo valido. controlla per favore"
			self.log.info(message)
			self.say(message)
		else:
			freshNews = feedparser.parse(self.address).entries

			if len(self.oldNews) == 0:
				toRead = freshNews[0:4]
			else:
				toRead = [i for i in freshNews if i not in self.oldNews]
			
			self.oldNews = freshNews
			greetings="su "+self.name+"."
			self.say(greetings)
			
			for news in toRead:
				digest = alviUtils.str_to_hlf(news.get('title'))
			#	print self.address + ':  '+digest
				self.log.info(self.address + ':  '+digest)
				self.say(digest)
			
	def __str__(self):
		return self.name+' '+self.address
