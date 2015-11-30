#!/usr/bin/env python
#-*- coding: UTF-8 -*-

'''
Parse wordlist file.
'''

import os


def WordList(fileName):
	if os.path.exists(fileName):
		with open(fileName, "r") as fd:
			for line in fd:
				if line and not line.startswith("#"):
					yield line.strip()