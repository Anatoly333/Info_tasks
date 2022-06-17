'''
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()
'''
'''
import argparse
parser = argparse.ArgumentParser()
parser.parse_args()
'''
'''
import sys
sys.argv
'''

'''
import pandas
import numpy as np
import pandas as pd
import csv
data = pandas.read_excel('history.xlsx')
lengt = len(data)
print(lengt)
'''


import argparse
import pandas
import numpy as np
import pandas as pd
import csv

parser = argparse.ArgumentParser()
parser.add_argument("FILE", type = str, help = 'First argument')
parser.add_argument("-C", "--num_columns", help = 'Number of  columns', action="store_true") 
parser.add_argument("-R", "--num_rows", help = 'Number of  rows', action="store_true") 
parser.add_argument("-a", "--all", help = 'All gile', action="store_true") 
args = parser.parse_args()
	
	
def num_rows(FILE: str):
	data = pandas.read_excel('{}'.format(FILE))
	lengt = len(data)
	print(lengt + 1)

def num_columns(FILE: str):
	data = pandas.read_excel('{}'.format(FILE))
	row_count = sum(1 for row in data)
	print(row_count)

def all(FILE: str):
	data = pandas.read_excel('{}'.format(FILE))
	print(data)
	
if args.num_columns:
	num_columns(args.FILE)
if args.num_rows:
	num_rows(args.FILE)
if args.all:
	all(args.FILE)
'''
parser2 = argparse.ArgumentParser()
parser2.add_argument("FILE", type = str, help = 'First argument')
parser2.add_argument("index", type = int, help = 'Second argument')
parser2.add_argument("-r", "--row_index", help = 'row by index', action="store_true") 

args2 = parser2.parse_args()

	
def row_index(FILE: str, index: int):
	data = pandas.read_excel('{}'.format(FILE))
	row = data.iloc[index]
	print(row)
	
if args2.row_index:
	row_index(args2.FILE, args2.index)

'''
'''
parser3 = argparse.ArgumentParser()
parser3.add_argument("FILE", type = str, help = 'First argument')
parser3.add_argument("name", type = str, help = 'Second argument')
parser3.add_argument("-c", "--column", help = 'column by name', action="store_true") 

args3 = parser3.parse_args()

	
def column(FILE: str, name: str):
	data = pandas.read_excel('{}'.format(FILE))
	column = data[name]
	print(column)
	
if args3.column:
	column(args3.FILE, args3.name)


if args3.column and args2.row_index:
	print('KeyError')
'''
