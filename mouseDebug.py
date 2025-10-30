import json

def capabilities_dump(cap):
	for key in cap.keys():
		print(f'{key}:{cap[key]}')

def JDUMP(d,title=None,pause=None):
	if title:
		print(f'{title}')
	print(json.dumps(d,indent=4))
	if pause:
		input(pause)

def dict_dump(dct:dict,title=None,pause=None):
	if title:
		print(f'{title}')
	keys=dct.keys()
	long_key=0
	for k in keys:
		l=len(k)
		if l > long_key:
			long_key=l