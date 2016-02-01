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
import os
import tempfile
import subprocess
import wave
import urllib
import urlparse
import requests
from abc import ABCMeta, abstractmethod


import gtts
import mad
		


class speech:

	def __init__(self):
		self.festival = True
		self.espeak = False

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
			#self.f = festival.open()
			festival.say(text)
		elif self.espeak:
			espeakTTS.say(text)
		else:
			self.google_say(text)

	def google_say(self, text):
		tts = gtts.gTTS(text=text, lang='en')
		with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
			tmpfile=f.name
		tts.save(tmpfile)
		mf = mad.MadFile(tmpfile)
		with tempfile.NamedTemporaryFile(suffix='.wav') as f:
			wav = wave.open(f, mode='wb')
			wav.setframerate(mf.samplerate())
			wav.setnchannels(1 if mf.mode() == mad.MODE_SINGLE_CHANNEL else 2)
			wav.setsampwidth(4L)
			frame = mf.read()
			while frame is not None:
				wav.writeframes(frame)
				frame = mf.read()
			wav.close()
			cmd = ['aplay', '-D', 'plughw:1,0', str(tmpfile)]
			with tempfile.TemporaryFile() as fw:
				subprocess.call(cmd, stdout=fw, stderr=fw)

		os.remove(tmpfile)

