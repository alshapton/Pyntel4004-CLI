# Import system libraries
import os
import sys

# Import resources library (part of setuptools)
import pkg_resources

# Import click library
import click

# Import Pyntel4004 functionality
from assembler.assemble import assemble
from disassembler.disassemble import disassemble
from executer.execute import execute
from executer.exe_supporting import retrieve
from hardware.processor import Processor
from shared.shared import print_messages

package = "Pyntel4004-cli"
core_name = 'Pyntel4004'
cini = core_name + ' core is not installed - use \n\n' + \
        '       pip install ' + core_name + '\n'
module = os.path.basename(sys.argv[0])
__version__ = pkg_resources.require(package)[0].version
__Pyntel4004_version__ = 'Installed'

try:
    __Pyntel4004_version__ = pkg_resources.require(core_name)[0].version
except:
    __Pyntel4004_version__ = 'Not Installed'
else:
    __Pyntel4004_version__ = 'Installed but no legal version'


def is_core_installed(package_name: str):
    """
    Check to see if the Pyntel4004 core is installed

    Parameters
    ----------
    package_name: str, mandatory
        Name of the Pyntel4004 core package

    Returns
    -------
    True    - if the core package is installed
    False   - if not

    Raises
    ------
    N/A

    Notes
    -----
    N/A

    """
    import importlib.util
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return False
    else:
        return True


@click.group()
@click.help_option('--help', '-h')
@click.version_option(__version__, '--version', '-v',
                      prog_name=package + ' (' + module + ')',
                      message='%(prog)s, Version %(version)s \nPyntel4004 ' +
                      'Version: ' + __Pyntel4004_version__ + '\n' +
                      'Learn more at https://github.com/alshapton/Pyntel4004')
@click.pass_context
def cli(ctx):
    '''
    Command Line Interface (CLI) for Pyntel4004,
    a virtual Intel© 4004 processor written in Python.

    Learn more at https://github.com/alshapton/Pyntel4004
    '''
    pass


@cli.command()
@click.option('--input', '-i', prompt='Input file:',
              help='4004 assembler source code.', required=True,
              type=str, metavar='<filename>')
@click.option('--output', '-o', prompt='Output file:',
              help='4004 output file.', default='4004.out',
              metavar='<filename>')
@click.option('--exec', '-x', is_flag=True, help='Execute program')
@click.option('--quiet', '-q', is_flag=True,
              help='Output on/off  [either/or   ]')
@click.option('--monitor', '-m', is_flag=True,
              help='Monitor on/off [but not both]')
@click.help_option('--help', '-h')
def asm(input, output, exec, monitor, quiet):
    """Assemble the input file"""

    # Ensure that the core Pyntel4004 is installed
    # Exit if not
    if not is_core_installed(core_name):
        raise click.ClickException(cini)
    # Create new instance of a processor
    chip = Processor()
    # Check exclusiveness of parameters
    # Raise an error if not allowed
    if quiet and monitor:
        raise click.BadParameter("Invalid Parameter Combination: " +
                                 "--quiet and --monitor cannot be used " +
                                 "together\n")

    result = assemble(input, output, chip, quiet)
    if result and exec:
        print_messages(quiet, 'EXEC', chip, '')
        did_execute = execute(chip, 'rom', 0, monitor, quiet)
        if did_execute:
            print_messages(quiet, 'BLANK', chip, '')
            print_messages(quiet, 'ACC', chip, '')
            print_messages(quiet, 'CARRY', chip, '')
            print_messages(quiet, 'BLANK', chip, '')


@cli.command()
@click.option('--object', '-o', prompt='Object file:',
              help='4004 object or binary file (specify extension)',
              metavar='<filename>',
              required=True, type=str)
@click.option('--inst', '-i',
              help='Instuctions to disassemble',
              metavar='<Between 1 & 4096>',
              type=int)
@click.option('--labels', '-l',
              help='Show label table',
              is_flag=True, default=False)
@click.help_option('--help', '-h')
def dis(object, inst, labels) -> None:
    """Disassemble the input file"""
    # Ensure that the core Pyntel4004 is installed
    # Exit if not
    if not is_core_installed(core_name):
        raise click.ClickException(cini)
    if inst is None:
        inst = 4096
    else:
        if inst < 1 or inst > 4096:
            raise click.BadParameter("Instructions should be between " +
                                     "1 and 4096")
    # Create new instance of a processor
    chip = Processor()
    memory_space, _, lbls = retrieve(object, chip, False)
    disassemble(chip, memory_space, 0, inst, labels, lbls)


@cli.command()
@click.option('--object', '-o', prompt='Object file:',
              help='4004 object or binary file (specify extension)',
              metavar='<filename>',
              required=True, type=str)
@click.option('--quiet', '-q', is_flag=True,
              help='Output on/off')
@click.help_option('--help', '-h')
def exe(object, quiet):
    """Execute the object file"""
    # Ensure that the core Pyntel4004 is installed
    # Exit if not
    if not is_core_installed(core_name):
        raise click.ClickException(cini)
    # Create new instance of a processor
    chip = Processor()
    result = retrieve(object, chip, quiet)
    memory_space = result[0]
    execute(chip, memory_space, 0, False, quiet)
