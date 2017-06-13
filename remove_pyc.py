#coding: utf-8
import os
import sys


def	remove_pyc(filepath):
	for f in os.listdir(filepath):
		if ".pyc" in f:
			os.remove(filepath + "\\" + f)
		elif os.path.isdir(filepath + "\\" + f):
			remove_pyc(filepath + "\\" + f)

currentpath = os.getcwd()
remove_pyc(currentpath)

