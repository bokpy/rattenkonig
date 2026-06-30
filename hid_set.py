#!/bin/python3
import os
import json

from icecream import ic
ic.configureOutput(includeContext=True)


class HidSet(set):
	def __init__(S,filepath):
		super().__init__(S)
		S.filepath=filepath
		#print(f'HidSet("{filepath}")')
		
	def show(S):
		for item in S:
			print(f'{item}')
	
	def writeset(S):
		if len(S)==0:
			print(f'Not writing empty set "{S.filepath}"')
			return
		try:
			with open(S.filepath, 'w') as f:
				json.dump(list(S),f)
		except Exception as e:
			print(f'writing "{S.filepath}" failed')
			ic(e)
			exit(1)
	
	def readset(S):
		if not os.path.isfile(S.filepath):
			#print(f'No file "{S.filepath}"')
			return
			
		try:
			with open(S.filepath, 'r') as f:
				jsonlist=json.load(f)
		except Exception as e:
			print(f'Reading "{S.filepath}" failed.')
			ic(e)
			exit(1)
		for item in jsonlist:
			#print(f'\t{item=}')
			S.add(tuple(item))
	
	def stores_new(S,tup):
		"""
		store a tuple
		:return: True if new else False
		"""
		if tup in S:
			return False
		S.add(tup)
		return True
	
	def takeout(S, item1,item2):
		print(f' takeout({item1} , {item2}) ',end='')
		if item1 and item2:
			S.remove((item1,item2))
			print ( f' -1 -2')
			return
		if item1:
			for item in S:
				if item1==item[0]:
					S.remove(item)
					
					print ( f' -1 xx')
					return
			return
		if item2:
			for item in S:
				if item2==item[1]:
					S.remove(item)
					S.add((item[0],''))
					print ( f' xx -2')
					print (f'store: ({item[0]},"")')
					return


if __name__ == '__main__':
	print(f'No test: {__file__}')