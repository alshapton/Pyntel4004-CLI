# Import system libraries
import os
import sys

# Import resources library (part of setuptools)
import pkg_resources

# Import click library
import click

# Import Pyntel4004 functionality
from hardware.processor import Processor
from assembler.assemble import assemble
from disassembler.disassemble import disassemble
from executer.execute import execute
from executer.exe_supporting import retrieve
from shared.shared import print_messages

package = "Pyntel4004-cli"
module = os.path.basename(sys.argv[0])
__version__ = pkg_resources.require(package)[0].version
__Pyntel4004_version__ = pkg_resources.require('Pyntel4004')[0].version


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
@click.option('--byte', '-b',
              help='Bytes to disassemble',
              metavar='<Between 1 & 4096>',
              type=int)
@click.help_option('--help', '-h')
def dis(object, byte):
    """Disassemble the input file"""
    if byte is None:
        byte = 4096
    else:
        if byte < 1 or byte > 4096:
            raise click.BadParameter("Bytes should be between 1 and 4096")

    print('Disassembling ' + str(byte) + ' bytes')
    # Create new instance of a processor
    chip = Processor()
    result = retrieve(object, chip, True)
    memory_space = result[0]
    disassemble(chip, memory_space, 0)


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
    # Create new instance of a processor
    chip = Processor()
    result = retrieve(object, chip, quiet)
    memory_space = result[0]
    execute(chip, memory_space, 0, False, quiet)
