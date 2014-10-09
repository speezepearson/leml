from .chunkify import chunkify

def iter_processed_chunks(modules, format, string):
	delimiter_pairs = [m.delimiter_pair for m in modules]
	delimiter_pair_to_module = {m.delimiter_pair: m for m in modules}
	for (open, content, close) in chunkify(delimiter_pairs, string):
		if open is close is None:
			yield content
		else:
			module = delimiter_pair_to_module[(open, close)]
			yield module.create(format, content)

def compile(modules, format, string):
	return ''.join(iter_processed_chunks(modules, format, string))