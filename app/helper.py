from .arg_parser import ArgParser

import sys

class Helper:

    def __init__(self, parser: ArgParser) -> object:
        """

        :param parser: Parser
        """
        self.parser = parser
        self.args = sys.argv

        # Регистрируем флаг -g
        self.register_generate()
        self.register_printer()
        self.register_memory()
        self.register_file()

        self.parser.parse()
        self.args = {}

    def is_empty_argv(self):
        return not self.parser.is_any_passed()

    def register_file(self, helper=False):
        key: str = '-file'
        _help = '{}: Имя входного файла'.format(key)

        return print(_help) if helper else self.parser.add(key, str, 'store', _help)

    def register_memory(self, helper=False):
        key: str = '-memory'
        _help = '{}: задает ограничение на память'.format(key)

        return print(_help) if helper else self.parser.add(key, str, 'store', _help)
    def register_printer(self, helper = False):
        key: str = '-print'
        _help = '{}: Пишет файл в консоль, второй параметр имя файла'.format(key)

        return print(_help) if helper else self.parser.add(key, str, 'store', _help)

    def register_generate(self, helper = False):
        key: str = '-g'
        _help = '{}: Создает файл нужных размеров, второй параметр - размер (1GB, 10MB, 100MB)'.format(key)

        return print(_help) if helper else self.parser.add(key, str, 'store', _help)

    def register_help(self, helper= False):
        key: str = '-help'
        _help = '{}: Инфо о командах'.format(key)

        return print(_help) if helper else self.parser.add(key, str, 'store', _help)

    def print_help(self):
        self.register_generate(True)
        self.register_printer(True)
        self.register_memory(True)

    def is_generate(self):
        return self.parser.get('g')

    def is_printer(self):
        return self.parser.get('print')

    def is_memory(self):
        return self.parser.get('memory')

    def is_file(self):
        return self.parser.get('file')



