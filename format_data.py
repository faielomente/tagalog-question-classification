import os
import sys


def read():
	with open(os.path.abspath('files/pos_input.csv')) as f:
		for line in f:
			print line

