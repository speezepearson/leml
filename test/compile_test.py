import unittest
import markup
import os

test_modules_path = os.path.join(os.path.dirname(__file__), 'modules.json')
test_modules = markup.parse_modules_json(open(test_modules_path))

def compile(string, format='fmt'):
	return markup.compile(test_modules, format, string)

class TestCompile(unittest.TestCase):
	def test_emptiness(self):
		self.assertEqual(markup.compile([], 'fmt', ''), '')
		self.assertEqual(markup.compile([], 'fmt', '$math$'), '$math$')
		self.assertEqual(compile(''), '')

	def test_singletons(self):
		self.assertEqual(compile('no delimiters'), 'no delimiters')
		self.assertEqual(compile('<>'), 'angle()')

	def test_repeat(self):
		self.assertEqual(compile('<a><b>'), 'angle(a)angle(b)')

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

	def test_embedding(self):
		self.assertEqual(compile(r'{--x--}'), '')
		self.assertEqual(compile(r'{--x--}', 'show-comments'), '(comment: x)')

unittest.main()