#!/usr/bin/env python

###########################
#
#  A.L.V.I. Bot
#
#  manager.py: handle execution in background of all regular tasks
#
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 14/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################



import time, thread, threading


class Task(threading._Timer):
	""" Thans to James Kassemi for this class """
	def __init__(self, *args, **kwargs):
		threading._Timer.__init__(self, *args, **kwargs)
		self.setDaemon(True)

	def run(self):
		while True:
			self.finished.clear()
			self.finished.wait(self.interval)
			if not self.finished.isSet():
				self.function(*self.args, **self.kwargs)
			else:
				return
			self.finished.set()



class Manager:
	""" This class handle the execution of all regular task 
	    needed by our assistant """

	def runner(self):
		for t in self.immediateTasks:
			t()
			self.immediateTasks.remove(t)

	def __init__(self):
		self.tasks = []
		self.immediateTasks = []
		t = Task(1,self.runner,[],{})
		self.tasks.append(t)

	def dummy_f(self):
		pass


	def enqueue(self, interval, operation,args=[], kwargs={}):
		interval *=60
		t= Task(interval, operation, args, kwargs)
		self.tasks.append(t)


	def start(self):
		for t in self.tasks:
			thread.start_new_thread(t.run, ())
	
	def stop(self):
		for t in self.tasks:
			t.cancel()

	def immediate(self,func):
		self.immediateTasks.append(func);


def f(a):
	print a

if __name__ == "__main__":
	import sys
	
	m = Manager()
	m.enqueue(5,f, ([str("5 secondi")]))

	m.start()

	a=''
	while a.strip() != 'quit':
		a = sys.stdin.readline()
		print a
		if a.strip() == 'quit':
			m.stop()
	
	

