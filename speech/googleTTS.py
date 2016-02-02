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
	


def say(text):
	# Google TTS seems not to work anymore

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

