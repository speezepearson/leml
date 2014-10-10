class Module(object):
	def __init__(self, delimiter_pair, create, embed_functions={}):
		self.delimiter_pair = delimiter_pair
		self.create = create
		self.embed_functions = embed_functions

	def embed(self, format, string):
		if format in self.embed_functions:
			return self.embed_functions[format](string)
		if 'default' in self.embed_functions:
			return self.embed_functions['default'](string)
		return string

	def process(self, format, string):
		return self.embed(format, self.create(string))

from . import descriptions
