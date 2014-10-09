import unittest
import markup

test_modules = (
	markup.Module(('<', '>'), lambda _, s: 'angle({})'.format(s)),
	markup.Module(('$', '$'), lambda _, s: 'math({})'.format(s)),
	markup.Module(('{--', '--}'), lambda _, s: '')
)

def compile(string):
	return markup.compile(test_modules, 'fmt', string)

class TestCompile(unittest.TestCase):
	def test_emptiness(self):
		self.assertEqual(markup.compile([], 'fmt', ''), '')
		self.assertEqual(markup.compile([], 'fmt', '$math$'), '$math$')
		self.assertEqual(compile(''), '')

	def test_singletons(self):
		self.assertEqual(compile('no delimiters'), 'no delimiters')
		self.assertEqual(compile('<>'), 'angle()')
		self.assertEqual(compile('$content$'), 'math(content)')
		self.assertEqual(compile('{-- comment --}'), '')

	def test_escaping(self):
		self.assertEqual(compile(r'\<>'), r'<>')
		self.assertEqual(compile(r'\\<>'), r'\angle()')
		self.assertEqual(compile(r'\\\<>'), r'\<>')
		self.assertEqual(compile(r'\\\\<>'), r'\\angle()')

		self.assertEqual(compile(r'<\>>'), r'angle(>)')
		self.assertEqual(compile(r'<\\>>'), r'angle(\)>')
		self.assertEqual(compile(r'<\\\>>'), r'angle(\>)')
		self.assertEqual(compile(r'<\\\\>>'), r'angle(\\)>')

		self.assertEqual(compile(r'no \delimiter'), r'no \delimiter')
		self.assertEqual(compile(r'no \\delimiter'), r'no \\delimiter')
		self.assertEqual(compile(r'no \\\delimiter'), r'no \\\delimiter')

	def test_unpaired(self):
		self.assertEqual(compile(r'>'), r'>')
		with self.assertRaises(ValueError):
			compile(r'<')

	def test_nesting(self):
		self.assertEqual(compile(r'<$>'), 'angle($)')
		self.assertEqual(compile(r'<<>'), 'angle(<)')

unittest.main()