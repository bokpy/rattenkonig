#!/bin /python3
import os
import subprocess

def service_call(*args):
	try:
		info = subprocess.check_output(args)
	except subprocess.SubprocessError as e:
		print(f'{args} failed')
		print(f'is {args[0]} intalled?')
		print(f'subprocess.SubprocessError {e}')
		return None
	str_info = info.decode('utf-8')
	return str_info.splitlines()

def input_devices():
	dev_path_by_id  = '/dev/input/by-id/'
	devs_by_id  = [os.readlink(dev_path_by_id + p)
	               for p in os.listdir(dev_path_by_id)  ]
	dev_paths = [ '/dev/input/' + os.path.basename(p)
 for p in devs_by_id ]
	return dev_paths

def main():
	print(input_devices())

if __name__ == "__main__":
	main()