import re
import sys
import subprocess

class ParseError(ValueError):
	pass

class Chunk(object):
	def __init__(self, delimiter, content):
		self.delimiter = delimiter
		self.content = content

	def __repr__(self):
		return 'Chunk({!r}, {!r})'.format(self.delimiter, self.content)
	def __str__(self):
		return repr(self)

def break_plain_chunk(delimiters, string):
	delimiters_string = ''.join(re.escape(d) for d in delimiters)
	pattern = '[^{}]*'.format(delimiters_string) if delimiters else '.*'
	match = re.match(pattern, string, flags=re.DOTALL)
	content = match.group()
	chunk = Chunk(None, content)
	rest = string[match.end():]
	assert (not rest) or any(rest.startswith(d) for d in delimiters)
	return (chunk, rest)

def break_delimited_chunk(delimiters, string):
	delimiter_pattern = '|'.join(re.escape(d) for d in delimiters)
	pattern = r'(?P<delimiter>{delimiter})(?P<content>.*?)(?P=delimiter)'.format(delimiter=delimiter_pattern)
	match = re.match(pattern, string, flags=re.DOTALL)
	if match is None:
		raise ParseError(delimiters, string)
	delimiter = match.group('delimiter')
	content = match.group('content')
	chunk = Chunk(delimiter, content)
	return (chunk, string[match.end():])

def chunkify(delimiters, string):
	while string:
		(plain_chunk, string) = break_plain_chunk(delimiters, string)
		if plain_chunk.content:
			yield plain_chunk

		if not string:
			break

		(delimited_chunk, string) = break_delimited_chunk(delimiters, string)
		yield delimited_chunk

class Module(object):
	def __init__(self, delimiter, create):
		self.delimiter = delimiter
		self.create = create

	@classmethod
	def from_json_object(cls, obj):
		if 'delimiter' in obj:
			if 'create' in obj:
				return cls(delimiter=obj['delimiter'], create=eval(obj['create']))
			if 'create-script' in obj:
				command = obj['create-script']
				def f(fmt, s):
					# print("fmt = {!r}, s = {!r}".format(fmt, s))
					# print("command = {}".format(command))
					p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
					(out, err) = p.communicate(s.encode(sys.stdout.encoding))
					# TODO: check for p.returncode != 0
					return out.decode(sys.stdin.encoding)
				return cls(delimiter=obj['delimiter'], create=f)
		return obj



def compile(modules, format, string):
	delimiters = [m.delimiter for m in modules]
	delimiter_to_module = {m.delimiter: m for m in modules}
	for chunk in chunkify(delimiters, string):
		if chunk.delimiter is not None:
			module = delimiter_to_module[chunk.delimiter]
			yield module.create(format, chunk.content)
		else:
			yield chunk.content

if __name__ == '__main__':
	
	import argparse
	import json
	import sys

	parser = argparse.ArgumentParser()
	parser.add_argument('module_file')

	args = parser.parse_args()

	modules_dict = json.load(open(args.module_file), object_hook=Module.from_json_object)
	for x in modules_dict.values():
		if not isinstance(x, Module):
			raise RuntimeError('{!r} does not describe a Module')

	modules = modules_dict.values()

	print(''.join(compile(modules, 'txt', sys.stdin.read())))

	# ms = [Module('$', lambda f,s: ''.join(reversed(s))),
	#       Module('`', lambda f,s: '<{f}>{s}</{f}>'.format(f=f, s=s))]
	# print(''.join(compile(ms, 'fmt', 'word $second$ `third` `mix$ed`')))