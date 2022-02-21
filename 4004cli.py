# Import click library
import click

# Import Pyntel4004 functionality
from hardware.processor import Processor
from assembler.assemble import assemble
from disassembler.disassemble import disassemble
from executer.execute import execute
from shared.shared import print_messages, do_error


__version__ = '1.0'


@click.group()
@click.help_option('--help', '-h')
@click.version_option(__version__, '--version', '-v',
                      prog_name='Pyntel4004-CLI (4004)',
                      message='%(prog)s, Version %(version)s \n' +
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
              help='4004 output file.', metavar='<filename>')
@click.option('--exec', '-x', is_flag=True, help='Execute program')
@click.option('--quiet', '-q', is_flag=True, help='No output mode')
@click.option('--monitor', '-m', is_flag=True, help='Monitor on/off')
@click.help_option('--help', '-h')
def asm(input, output, exec, monitor, quiet):
    """Assemble the input file"""
    # Create new instance of a processor
    chip = Processor()
    # Check exclusiveness of parameters
    if quiet and monitor:
        do_error('4004: Invalid Parameter Combination: (' +
                 '--quiet and --monitor cannot be used together)')
        exit()

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
@click.option('--source', '-s', prompt='Source file:',
              help='4004 assembler source code.', required=True, type=str)
@click.option('--object', '-o', prompt='Object file:',
              help='4004 object file.')
def dis(source, object):
    """Disassemble the file"""

    # Create new instance of a processor
    chip = Processor()
    _ = disassemble(source, object, chip)
