import sys
import subprocess
import json
from .. import Module

def parse_function(json):
	if isinstance(json, str):
		return (lambda input: json.format(input=input))
	elif isinstance(json, dict):
		if 'script' in json:
			command = json['script']
			def create(input):
				# print("fmt = {!r}, s = {!r}".format(fmt, s))
				# print("command = {}".format(command))
				p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
				(out, err) = p.communicate(input.encode(sys.stdout.encoding))
				# TODO: check for p.returncode != 0
				return out.decode(sys.stdin.encoding)
			return create
		raise ValueError()
	raise ValueError()

def parse_delimiter_pair(json):
	if isinstance(json, str):
		return (json, json)
	if isinstance(json, list):
		if len(json) == 2:
			return tuple(json)
		raise ValueError()
	raise ValueError()

def parse_embed_functions(json):
	if not isinstance(json, dict):
		raise ValueError()
	return {key: parse_function(value) for key, value in json.items()}

def module_hook(obj):
	try:
		delimiter_pair = parse_delimiter_pair(obj['delimiters'])
		create = parse_function(obj['create'])
		embed_functions = parse_embed_functions(obj.get('embed', {}))
	except (KeyError, ValueError):
		return obj

	return Module(delimiter_pair=delimiter_pair, create=create, embed_functions=embed_functions)

def parse_modules(file):
	modules_dict = json.load(file, object_hook=module_hook)
	if not isinstance(modules_dict, dict):
		raise ValueError('module file should parse to an object (was {})'.format(type(modules_dict)))
	for name, module in modules_dict.items():
		if not isinstance(module, Module):
			raise RuntimeError('value for {!r} is not a valid module description'.format(name))
	return modules_dict.values()