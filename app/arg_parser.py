import argparse
import sys


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = []
    @staticmethod
    def is_any_passed() -> bool:
        return bool(len(sys.argv))

    def add(self, name, type, action='store', help = ""):
        self.parser.add_argument( name, type=type, action=action, help=help)

    def parse(self):
        self.args = self.parser.parse_args()

    def get(self, arg):
        return getattr( self.args, arg, '')