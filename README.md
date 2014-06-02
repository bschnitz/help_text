### Help Text (help\_text)

#### DESCRIPTION

Help Text (help\_text) is a python3 module based on the argparse module. it is
used to load help text from a json file, in order to make it possible to
seperate that text from the rest of the code. it also restricts the argparse
module to a very specific way of structuring the command, for which the help
text shall be provided. the provided example covers pretty much all, this module
can be used for.

Update:<br \>
it is now also possible to specify a yaml file as input for your help\_text
program. it is even possible to have a yaml file as source for your input, which
is converted to your .json input automatically. e.g. assume you specify help.json
as input file, but you really want to describe the text in yaml, since it is
better readable for human eyes, then you could tell the program, that it shall
convert help.json from help.yaml, everytime, it finds the help.yaml file to be
newer than help.json. so you can avoid having the program to import PyYAML
everytime it is executed, so that is relies only on standard python modules.
look at the example to see how this is done (and try to change or remove
the examples/data/help.yaml file).

#### LICENSE

'Help Text' is licensed under version 3 of the GNU General Public License.

#### EXAMPLE

an example can be found in examples. help.json is the definition of the help for
the help command (help.py).

To test this package on the fly, without installing it, You have to make sure,
that python knows, where to find the help\_text package when using the examples.
This can be done by specifying the PYTHONPATH environment variable (see the
manpage of the python program).

**in short:** *assuming, that You are in the directory where the help\_text
package directory is located* (this should also be the directory, where this
readme is located), You can do this:

    PYTHONPATH=. python3 examples/help.py help

    PYTHONPATH=. python3 examples/help.py help cry

    PYTHONPATH=. python3 examples/help.py cry help

    PYTHONPATH=. python3 examples/help.py cry help -l 20

#### CONTACT

Benjamin Schnitzler <benjaminschnitzler@googlemail.com>
