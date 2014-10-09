import re

def until_delim_pattern(delim_pattern):
	return r'(?s)(?P<text>^|.*?(?<=[^\\]))(?P<backslashes>(\\\\)*)(?P<delim>{delim})'.format(delim=delim_pattern)

def break_chunk(delim_pattern, string):
	pattern = until_delim_pattern(delim_pattern)
	m = re.match(pattern, string)
	if m is None:
		raise ValueError('unescaped delimiter not found')

	text = m.group('text')
	n_backslashes = len(m.group('backslashes'))
	full_text = text + (n_backslashes//2) * '\\'
	delim = m.group('delim')

	return (full_text, delim, string[m.end():])

def chunkify(delimiter_pairs, string):
	any_open_delim_pattern = '|'.join(re.escape(dp[0]) for dp in delimiter_pairs)
	close_delim_patterns = {dp[0]: re.escape(dp[1]) for dp in delimiter_pairs}
	while string:
		# read undelimited text and, if there is any, return it
		try:
			(text, open_delim, string) = break_chunk(any_open_delim_pattern, string)
		except ValueError:
			yield (None, string, None)
			break
		if text:
			yield (None, text, None)

		# read delimited text and return it
		(text, close_delim, string) = break_chunk(close_delim_patterns[open_delim], string)
		yield (open_delim, text, close_delim)
