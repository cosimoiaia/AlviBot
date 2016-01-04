#!/usr/bin/env python
###########################
#
#  A.L.V.I. Bot
#
# AlviUtils.py: Class with varius formatting and parsing methods used by Alvi 
#
# Author: Cosimo Iaia  <cosimo.iaia@gmail.com>
# Date: 21/02/2010
#
# This file is distribuited under the terms of GNU General Public
# Copyright 2010 Cosimo Iaia
#
#
###########################

import string,unicodedata


transform_table = {
	'<': ' ',
	'>': ' ',
	'+': ' plus ',
	'-': ' minus ',
	'#': ' ',
	'$': ' dollar ',
	'^': ' ',
	'&': ' e ',
	'(': ',',
	')': ',',
	'=':' equals ',
	'_': ' ',
	'*': ' ',
	'/': ' ',
	'\\':' ',
	'@': ' @ ',
	'.': ' . ',
	'"': ' ',
	'~': ' ',
	'%': ' percent ',
	'^':' '

}


def str_to_hlf(string):
	""" Take a string and return it in a Human Listenable Format """
	str = unicodedata.normalize('NFKD', string).encode("ascii", "replace").replace('?', '')
	
	for ch in transform_table.keys():
		str = str.replace(ch, transform_table[ch])
	return str



if __name__ == "__main__":
	import sys
	print str_to_hlf(unicode(sys.argv[1]))
