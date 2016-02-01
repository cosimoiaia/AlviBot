import socket
import os
import time
import atexit
import signal


import tempfile
import subprocess

def say(text):
	cmd = ['text2wave']
	with tempfile.NamedTemporaryFile(suffix='.wav') as out_f:
		with tempfile.SpooledTemporaryFile() as in_f:
			in_f.write(text.strip())
			in_f.seek(0)
			with tempfile.SpooledTemporaryFile() as err_f:
    				subprocess.call(cmd, stdin=in_f, stdout=out_f,stderr=err_f)
    				err_f.seek(0)
		play=['aplay', str(out_f.name)]
		with tempfile.TemporaryFile() as f:
			subprocess.call(play, stdout=f, stderr=f)
	
