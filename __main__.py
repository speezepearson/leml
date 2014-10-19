import argparse
import sys

import markup

parser = argparse.ArgumentParser()
parser.add_argument('module_file')
parser.add_argument('source', nargs="?")
parser.add_argument('-f', '--format')

args = parser.parse_args()

modules = markup.parse_modules_json(open(args.module_file))

format = (args.format if args.format is not None
	      else args.source.rsplit('.', 1)[-1] if (args.source is not None and '.' in args.source)
	      else 'txt')
source = sys.stdin if args.source is None else open(args.source)

print(markup.compile(modules, format, source.read()))