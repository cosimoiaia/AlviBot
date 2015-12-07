#!/usr/bin/env python

import aiml


class AlviBrain():
	"""
		Python Class for AIML Brain's Alvi. Follow the white rabbit. :-)
	"""
	def __init__(self):
		self.brain = aiml.Kernel()
		self.brain.setPredicate("secure", "yes")
		self.brain.bootstrap(learnFiles="startup.xml", commands="bootstrap")
		self.brain.setPredicate("secure", "no")
		self.brain.setBotPredicate("name","Alvi")

	def answer(self, message):
		"""
		Return answer for the user!
		"""
		answer = self.brain.respond(message)
		return answer

	def reload(self):
		self.__init__()


if __name__ == "__main__":
	import sys
	brain = AlviBrain()
	while True:
		message = raw_input("Alvi > ")
		if message.strip() == 'reload':
			print "reloading..."
			brain.reload()
		else:
			answer = brain.answer(message)
			print answer
#		say(answer)


