#!/usr/bin/env python
###########################
#
#  A.L.V.I. Bot
#
# espeakTTS.py: wrapper for the eSpeak engine
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 12/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################




from espeak import espeak


def say(text):
	espeak.synth(text)
