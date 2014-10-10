import argparse
import sys

import markup

parser = argparse.ArgumentParser()
parser.add_argument('module_file')
parser.add_argument('-f', '--format', default='txt')

args = parser.parse_args()

modules = markup.parse_modules_json(open(args.module_file))

print(*markup.compile(modules, args.format, sys.stdin.read()), sep='', end='')
