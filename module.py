import sys
import subprocess

class Module(object):
	def __init__(self, delimiter_pair, create):
		self.delimiter_pair = delimiter_pair
		self.create = create

	@classmethod
	def from_json_object(cls, obj):
		# try to get a delimiter pair out of it
		if 'open' in obj and 'close' in obj:
			delimiter_pair = (obj['open'], obj['close'])
		elif 'delimiter' in obj:
			delimiter_pair = (obj['delimiter'], obj['delimiter'])
		else:
			return obj

		# try to get a create-function out of it
		if 'create' in obj:
			create = eval(obj['create'])
		elif 'create-script' in obj:
			command = obj['create-script']
			def create(fmt, s):
				# print("fmt = {!r}, s = {!r}".format(fmt, s))
				# print("command = {}".format(command))
				p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
				(out, err) = p.communicate(s.encode(sys.stdout.encoding))
				# TODO: check for p.returncode != 0
				return out.decode(sys.stdin.encoding)
		else:
			return obj

		return cls(delimiter_pair=delimiter_pair, create=create)
