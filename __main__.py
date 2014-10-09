import argparse
import json
import sys

from markup import Module, compile

parser = argparse.ArgumentParser()
parser.add_argument('module_file')
parser.add_argument('-f', '--format', default='txt')

args = parser.parse_args()

modules_dict = json.load(open(args.module_file), object_hook=Module.from_json_object)
if not isinstance(modules_dict, dict):
	raise ValueError('module file should be an object (was {})'.format(type(modules_dict)))
for name, module in modules_dict.items():
	if not isinstance(module, Module):
		raise RuntimeError('value for {!r} is not a valid module description'.format(name))

modules = modules_dict.values()

print(*compile(modules, args.format, sys.stdin.read()), sep='', end='')
