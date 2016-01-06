#!/usr/bin/env python
###########################
#
#  A.L.V.I. Bot
#
# speech.py: general wrapper for the TTS engines
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 12/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################

class speech:

	def __init__(self):
		self.festival = False
		self.espeak = True

		try:
			import festival
		except:
			self.festival=False
		
		try:
			import espeakTTS
		except:
			self.espeak=False
		

	def say(self, text):
		if self.festival:
			self.f = festival.open()
			self.f.say(text)
		else:
			espeakTTS.say(text)

