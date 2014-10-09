import re

def _backslash_halver(match):
	return (len(match.group('backslashes'))//2) * '\\' + match.group('pattern')
def deescape(pattern, string):
	backslashes_then_pattern = r'\\(?P<backslashes>(\\\\)*)(?P<pattern>{})'.format(pattern)
	return re.sub(backslashes_then_pattern, _backslash_halver, string)

def break_chunk(delim_pattern, string):
	# Find the pattern, preceded by an even number of backslashes.
	pattern = r'(?s)(?P<nominal>.*?)(?<!\\)(?P<backslashes>(\\\\)*)(?P<delim>{})'.format(delim_pattern)
	m = re.match(pattern, string)

	if m is None:
		# Not found.
		escaped = string
		backslashes = ''
		delim = None
		remainder = ''
	else:
		escaped = m.group('nominal')
		backslashes = len(m.group('backslashes'))//2 * '\\'
		delim = m.group('delim')
		remainder = string[m.end():]
	deescaped = deescape(delim_pattern, escaped)
	return (deescaped+backslashes, delim, remainder)

def chunkify(delimiter_pairs, string):
	if not delimiter_pairs:
		yield (None, string, None)
		return
	any_open_delim_pattern = '|'.join(re.escape(dp[0]) for dp in delimiter_pairs)
	close_delim_patterns = {dp[0]: re.escape(dp[1]) for dp in delimiter_pairs}
	while string:
		# read undelimited text and, if there is any, return it
		(text, open_delim, string) = break_chunk(any_open_delim_pattern, string)

		if text:
			yield (None, text, None)

		if open_delim is None:
			break

		if not open_delim:
			raise RuntimeError("any_open_delim_pattern = {!r}".format(any_open_delim_pattern))
		# read delimited text and return it
		(text, close_delim, string) = break_chunk(close_delim_patterns[open_delim], string)
		if close_delim is None:
			raise ValueError()
		yield (open_delim, text, close_delim)
