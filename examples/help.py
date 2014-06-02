#!/usr/bin/env python3

import os
import sys

from help_text.help_text import HelpText

class Help:
  def __init__(self):
    data_path = os.path.dirname(__file__) + "/data"
    self.help_text = HelpText(
        help_file=data_path + "/help.json",
        argv=sys.argv,
        convert_from=data_path + "/help.yaml"
    )
    self.help_text.set_handle( self.cry, "cry" )

  def execute(self):
    self.help_text.parse_and_exec()

  def cry(self, args):
    what = args.what
    if args.loudness > 0:
      if args.loudness < 10:
        pass
      elif args.loudness < 20:
        what = what[0].upper() + what[1:]
      elif args.loudness < 30:
        what = what.upper() + " !"
      elif args.loudness < 40:
        what = what.upper() + " !!!"
      print(what)

cmd = Help()
cmd.execute()
