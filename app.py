from app.generator import Generator
from app.printer import BinaryPrinter
from app.reader import BinaryReader

from app.arg_parser import ArgParser

if __name__ == 'main':
    parser = ArgParser()

    if parser.is_any_passed() is False:
        Generator(file_size='1GB', array_size=1000).generate()

    BinaryReader().read()