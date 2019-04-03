from app.generator import Generator
from app.printer import Printer

from app.arg_parser import ArgParser
from app.helper import Helper

parser = ArgParser()
helper = Helper(parser)


if __name__ == '__main__':
    # Никаких аргументов не пришло
    if helper.is_empty_argv():
        exit(helper.print_help())

    #флаг g
    if helper.is_generate():
        size = helper.is_generate()
        Generator(file_size=size, array_size=1000).generate()

    #флаг -print
    if helper.is_printer():
        fname = helper.is_printer()
        Printer(file_name=fname, how_many=1000).print()

    # Флаг -memory
    # Default:1MB RAM
    memory = 1024 * 1024 * 1
    if helper.is_memory():
        memory = helper.is_memory()

    file = 'data_temp'
    if helper.is_file():
        file = helper.is_file()





