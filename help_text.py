# Copyright 2014 Benjamin Schnitzler <benjaminschnitzler@googlemail.com>

# help_text 
# 
# help_text is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# help_text is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with help_text. If not, see <http://www.gnu.org/licenses/>.

import json
from argparse import ArgumentParser

class HelpText():
  types = { 'str':str, 'int':int }
  def __init__(self, **kwargs):
    self.argv = kwargs['argv']
    self.create_argument_parsers(kwargs['help_file'])

  def create_argument_parsers( self, json_file ):
    self.parser = ArgumentParser()
    self.set_handle( self.print_help )
    self.parsers = {}
    with open( json_file, 'r' ) as fh:
      arg_txt = json.load(fh)
      if 'subcommands' in arg_txt:
        sub_sec = arg_txt['subcommands']
        description = sub_sec['description']
        if type(description) == list: description = " ".join(description)
        description = description.format( script=self.argv[0] )
        subparsers = self.parser.add_subparsers( description=description )
        for cmd in sub_sec['commands']: self.add_command(cmd, subparsers)
        if 'help' in self.parsers: self.set_handle( self.print_help, 'help' )

  def add_command( self, command, subparsers ):
    arguments = command.pop('arguments')
    sub_parser = subparsers.add_parser( **command )
    sub_parser.set_defaults( func=self.not_implemented_yet )
    for arg in arguments:
      options = map( lambda s: s.strip(), arg['options'].split(',') )
      arg.pop('options')
      self.convert_type_field(arg)
      sub_parser.add_argument(*options, **arg)
    self.parsers[command['name']] = sub_parser

  def convert_type_field(self, args):
    if 'type' in args:
      # we could just use eval here... but making eval safe is difficult,
      # so let's better avoid any risk by using a type checking dictionary
      args['type'] = self.types[args['type']]

  def set_handle( self, func, subcmd=None ):
    if subcmd != None: self.parsers[subcmd].set_defaults( func=func )
    else:              self.default_handle = func

  def not_implemented_yet(self, args):
    print("Not implemented yet.")

  def print_help(self, args):
    if 'cmd' in args and args.cmd != None:
      self.parsers[args.cmd].print_help()
    else: self.parser.print_help()

  def parse_and_exec(self):
    args = self.parser.parse_args(self.argv[1:])
    if not 'func' in args: args.func = self.default_handle
    args.func(args)
