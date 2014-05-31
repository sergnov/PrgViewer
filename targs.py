#__encoding=utf-8
#Программа для визуализации файлов PRG
#2013.0.0.2
#Поддерживается формат v2

import argparse

parser = argparse.ArgumentParser(description='Generate png with prg')
parser.add_argument('-a', '--auto', action='store_true', help='auto default generation')
parser.add_argument('-ifl', '--input_file', action='store' , help='path to prg file')
parser.add_argument('-ofl', '--output_file', action='store' , help='path to new png file')
args = parser.parse_args()

if args.auto:
	print('AUTO Processing')
else:
	if args.input_file!=None:
		print(args.input_file)
	if args.output_file!=None:
		print(args.output_file)