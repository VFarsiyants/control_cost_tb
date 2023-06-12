import argparse
import os
import sys
import importlib

parser = argparse.ArgumentParser()
commands = os.listdir('commands')
commands.remove('__init__.py')

try:
    commands.remove('__pycache__')
except ValueError:
    pass

FUNCTION_MAP = dict()

for command in commands:
    command_file = command.split('.')[0]
    module = importlib.import_module(f'commands.{command_file}')
    handle_class = getattr(module, 'HandleCommand')
    FUNCTION_MAP[command_file] = getattr(handle_class, 'command')

command_name = ''

try:
    command_name = sys.argv[1]
except IndexError:
    pass

if command_name in FUNCTION_MAP:
    FUNCTION_MAP[command_name]()
    print('command executed')
else:
    print('Uknown command')
