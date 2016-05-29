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

import os, sys
import json
from argparse import ArgumentParser
from importlib import import_module

class HelpText():
  def __init__(self, **kwargs):
    """ Initialize the HelpText Object

    Kwargs:
        argv - required:
            the argument vector to parse. this should usually be sys.argv.
        help_file - required:
            the path to the help text file from which the help text is read.
        use_yaml:
            if set and True, the help text file will be parsed as YAML-file.
            this requires the PyYAML package to be installed. if not set or
            False, the python yaml module is used to parse the help text file.
        convert_from:
            if this is set, it will be assumed to be the path of a file (the
            source file), in which the actual help text file content is stored.
            it also means, that this content is converted and placed in to the
            help text file (specified by help_file).
            if use_yaml is set to True, the source file is assumed to be a json
            file, which shall be converted to yaml, otherwise the :
            format will be json, else yaml. the conversion only takes place, if
            the modification time of the destination file is greater or equal to
            the modification time of the original help text file. the content of
            the original file remains untouched (if it is not identical to the
            destination file). the PyYAML package has to be installed for this
            to work.
    """
    self.argv = kwargs['argv']
    use_yaml  = kwargs.get('use_yaml', False)
    self.help_file = kwargs['help_file']

    self.format_args = []
    self.format_kwargs = {}

    self.text_parser = import_module('yaml') if use_yaml else json

    self.conv_from = kwargs.get('convert_from', None)
    if self.conv_from != None: self.convert( use_yaml )

    self.create_argument_parsers()

  def convert( self, use_yaml ):
    if not os.path.exists(self.help_file) or\
       os.path.getmtime(self.conv_from) >= os.path.getmtime(self.help_file):
      converter = json if use_yaml else import_module('yaml')
      with open( self.conv_from, 'r' ) as fh:
        arg_txt = converter.load(fh)
      with open( self.help_file, 'w' ) as dst:
        if use_yaml: self.text_parser.dump( arg_txt, dst, allow_unicode=True )
        else:  self.text_parser.dump( arg_txt, dst, ensure_ascii=0, indent=4 )

  def create_argument_parsers( self ):
    self.parser = ArgumentParser()
    self.set_handle( self.print_help )
    self.parsers = {}
    with open( self.help_file, 'r' ) as fh:
      self.arg_txt = self.text_parser.load(fh)

  def add_command( self, command, subparsers ):
    arguments = command.pop('arguments', [])
    if 'description' in command and type(command['description']) == list:
      command['description'] = " ".join(command['description'])
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
      types = { 'str':str, 'int':int }
      args['type'] = types[args['type']]

  def set_handle( self, func, subcmd=None ):
    if subcmd != None: self.parsers[subcmd].set_defaults( func=func )
    else:              self.default_handle = func

  def not_implemented_yet(self, args):
    print("Not implemented yet.", file=sys.stderr)

  def print_help(self, args):
    if 'cmd' in args and args.cmd != None:
      cmd = args.cmd[0] if type(args.cmd) == list else args.cmd
      self.parsers[cmd].print_help()
    else: self.parser.print_help()
    
    """ preparse the help text, which was read during initialization

    this function will parse all text that was read from the help text file and
    use string.format with the arguments specified in self.set_format. it will
    also preparse the text for the use with the argparse module.
    """

  def set_format( self, *args, **kwargs ):
    """ string.format is called on the variable text fields (description,
        metavar, help) in the commands and subcommands sections of the help text
        file, using the parameters provided with this function.
    """
    self.format_args = args
    self.format_kwargs = kwargs

  def format( self, command, key ):
    """ formats command[key] using the format specified with set_format """
    command[key] = command[key].format(
      *self.format_args,
      **self.format_kwargs
    )

  def preparse_command( self, command ):
    """ preparses the variable text fields of the help text command definition

        positional arguments:

            command
                subsection of subcommands or commands from the help text file,
                stored in a dictionary.
    """
    for key in [ 'description', 'help', 'metavar' ]:
      if key in command:
        if type(command[key]) == list:
          command[key] = " ".join( command[text] )
        self.format( command, key )

  def preparse_help_text( self ):
    """ formatting of the help text and initialization of the arparse parser """
    if 'subcommands' in self.arg_txt:
      sub_sec = self.arg_txt['subcommands']
      commands = sub_sec.pop( 'commands', {} )
      self.preparse_command( sub_sec )
      subparsers = self.parser.add_subparsers( **sub_sec )
      for cmd in commands:
        self.add_command( cmd, subparsers )
      if 'help' in self.parsers:
        self.set_handle( self.print_help, 'help' )

  def parse_and_exec(self):
    self.preparse_help_text()
    args = self.parser.parse_args(self.argv[1:])
    if not 'func' in args: args.func = self.default_handle
    args.func(args)
