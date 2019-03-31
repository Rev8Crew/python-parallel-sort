import argparse

parser = argparse.ArgumentParser('Simple Arg Parser')

parser.add_argument('-m', '--memory', action='store', help='Макс выделенная память')
parser.add_argument('-f', '--file', action='store', help='Имя файла')

parser.parse_args()

# Имя входного файла
file_name = parser.file
# ПО дефолту 1 GB RAM
memory = parser.memory if parser.memory else 1024*1024*1024