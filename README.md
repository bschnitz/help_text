### help\_text 

#### DESCRIPTION

help\_text is a python module based on the argparse module. it is used to
load help text from a json file to make it able to seperate that text from the
rest of the code. it also restricts the argparse module to a very specific way
of structuring the command, for which the help text shall be provided. the
provided example covers pretty much all, this module can be used for.

#### EXAMPLE

an example can be found in examples. help.json is the definition of the help for the help command (help.py). try the following examples:

    help.py help

    help.py help cry

    help.py cry help

    help.py cry help -l 20

#### FUTURE VISIONS

- make it possible to alternatively load the help text from a yaml file using
  this great PyYAML package, since it is really no joy for a human to
  write/debug json files.

#### LICENSE

help\_text is licensed under version 3 of the GNU General Public License.
