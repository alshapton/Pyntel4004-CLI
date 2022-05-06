# Import system libraries
import os
import sys

# Import resources library (part of setuptools)
import pkg_resources

# Import toml library
import toml
from toml import TomlDecodeError

# Import click library
import click

# Import Pyntel4004 functionality
from assembler.assemble import assemble
from disassembler.disassemble import disassemble
from executer.execute import execute
from executer.exe_supporting import retrieve
from hardware.processor import Processor
from shared.shared import print_messages, coredump


class Error(Exception):
    """Base class for other exceptions"""


class CoreNotInstalled(Error):
    """Exception for when Pyntel4004 is not installed"""


class ConfigFileNotFound(Error):
    """Exception for when the configuration file specified cannot be found"""


class BadFormat(Error):
    """Exception for when the configuration file is badly formatted"""


def excepthook(exc, value, traceback):
    print(value)


global package, core_name, cini
package = "Pyntel4004-cli"
core_name = 'Pyntel4004'
cini = '\n\n' + core_name + ' core is not installed - use \n\n' + \
    '       pip install ' + core_name + '\n'

sys.excepthook = excepthook


# ----------- Check Functionality ----------- #

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


def check_quiet(quiet, configuration):
    if quiet is None:
        if "quiet" in configuration:
            quiet = configuration["quiet"]
        else:
            quiet = False
    else:
        quiet = True
    return quiet


def check_exec(exec, configuration):
    if exec is None:
        if "exec" in configuration:
            exec = configuration["exec"]
        else:
            exec = False
    else:
        exec = True
    return exec


def check_inst(inst):
    if inst is None:
        inst = 4096
    else:
        if inst < 1 or inst > 4096:
            raise click.BadOptionUsage("--inst", "Instructions should be" +
                                       "between 1 and 4096")
    return inst


def check_monitor(monitor, configuration):
    if monitor is None:
        if "monitor" in configuration:
            monitor = configuration["monitor"]
        else:
            monitor = False
    else:
        monitor = True
    return monitor


def check_results_content(configuration):
    if "show" in configuration:
        show = configuration["show"]
        if show is None:
            show = "['ALL']"
    return show


def check_dis_content(configuration, object, inst, labels):
    if "object" in configuration and object is None:
        object_file = configuration["object"]
        if object_file is None:
            raise click.BadOptionUsage(
                "--object/--config", "No object file specified\n")
        if "inst" in configuration and inst is None:
            inst = configuration["inst"]
        if labels is False and "labels" in configuration:
            labels = configuration["labels"]
        else:
            labels = True
    return object_file, inst, labels


def check_asm_content(configuration, input_file, output, type_type):
    if "input" in configuration and input_file is None:
        input_file = configuration["input"]
    if "output" in configuration and output == 'default':
        output = configuration["output"]
    if "type" in configuration and type_type == ('None',):
        type_type = configuration["type"]
    if input_file is None and output == 'default' \
            and type_type == ('None',):
        raise click.BadOptionUsage(
            "--config", "Empty 'asm' section in configuration file\n")
    return input_file, output, type_type


def check_type(type_type):
    # Check --type parameters
    # Raise error if not valid
    good = True
    all_found = False
    for i in type_type:
        if i.upper() in ('ALL', ):
            all_found = True
        if i.upper() not in ('ALL', 'OBJ', 'H', 'BIN'):
            good = False
    if good is False:
        raise click.BadOptionUsage("--type", "Invalid output type specified\n")

    # Check --type parameters - ALL cannot be specified with others
    # Raise error if not valid
    if all_found:
        others = True
        for i in type_type:
            if i.upper() in ('OBJ', 'H', 'BIN'):
                others = False
        if others is False:
            raise click.BadOptionUsage("--type", "Cannot specify 'ALL' " +
                                       "with any others\n")

# ----------- Utility Functionality ----------- #


def getversion(name: str):
    __version__ = 'Installed'
    try:
        __version__ = pkg_resources.require(name)[0].version
    except CoreNotInstalled:
        __version__ = 'Not Installed'
    else:
        __version__ = 'Installed but no legal version'
    return __version__


def get_config(toml_file: str):
    """
    Retrieve a configuration file

    Parameters
    ----------
    toml_file: str, mandatory
        Name of the configuration file

    Returns
    -------
    configuration: str
        String containing the configuration data

    Raises
    ------
    ConfigFileNotFound - the file cannot be opened
    BadFormat - The configuration file is badly formatted TOML

    Notes
    -----
    N/A

    """
    configuration = None
    try:
        _ = open(toml_file)
    except OSError as e:
        if str(e.strerror[0:12]) == 'No such file':
            raise ConfigFileNotFound('Error:Configuration file not found.')
    try:
        configuration = toml.load(toml_file)
    except (TypeError, TomlDecodeError):
        raise BadFormat('Badly formatted configuration file')
    return configuration


# --------- Extended Functionality --------- #


def print_extended_results(chip: Processor, requirements) -> None:
    if requirements is None or requirements == []:
        return

# ----------- Main Functionality ----------- #


@click.group()
@click.help_option('--help', '-h')
@click.version_option(pkg_resources.require(package)[0].version,
                      '--version', '-v', prog_name=package + ' (' +
                      os.path.basename(sys.argv[0]) + ')',
                      message='%(prog)s, Version %(version)s \n' + core_name
                      + ' ' + 'Version: ' + getversion(core_name) + '\n' +
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
@click.help_option('--help', '-h')
@click.option('--input', '-i',
              help='4004 assembler source code.',
              type=str, metavar='<filename>')
@click.option('--output', '-o',
              help='4004 output file (without extension).', default='default',
              metavar='<filename>')
@click.option('--exec', '-x', is_flag=True, help='Execute program',
              default=None)
@click.option('--type', '-t', multiple=True, default=['None'],
              metavar='<extension>',
              help='Multiple output types can be specified - bin/obj/h/ALL')
@click.option('--config', '-c', metavar='<filename>',
              help='Configuration file', default='')
@click.option('--quiet', '-q', is_flag=True, default=None,
              help='Output on/off    [Either/Or,  ]')
@click.option('--monitor', '-m', is_flag=True, default=None,
              help='Monitor on/off   [but not both]')
@click.option('--results', '-r', is_flag=True, default=None,
              help='Results on/off')
def asm(input, output, exec, monitor, quiet, type, config, results):
    """Assemble the input file"""
    # Eliminate the "Shadowing" of builtins
    input_file = input
    type_type = type

    # Ensure that the core Pyntel4004 is installed
    # Exit if not
    if not is_core_installed(core_name):
        raise CoreNotInstalled(cini)

    # Get configuration (override from command line if required)
    if config is not None:
        configuration = get_config(config)
        show = check_results_content(configuration["results"])
        if "asm" in configuration:
            asm_configuration = configuration["asm"]
            input_file, output, type_type = \
                check_asm_content(asm_configuration, input_file,
                                  output, type_type)
            exec = check_exec(exec, asm_configuration)
            monitor = check_monitor(monitor, asm_configuration)
            quiet = check_quiet(quiet, asm_configuration)
        else:
            raise click.BadOptionUsage(
                "--config", "No 'asm' section in configuration file\n")
    else:
        show = "['ALL']"
    # Create new instance of a processor
    chip = Processor()
    # Check exclusiveness of parameters
    # Raise an error if not allowed
    if quiet and monitor:
        raise click.BadParameter("Invalid Parameter Combination: " +
                                 "--quiet and --monitor cannot be used " +
                                 "together\n")
    # Check existence of --type parameter
    # Raise error if not present
    if type_type == ('None',):
        raise click.BadOptionUsage("--type", "No output type specified\n")
    check_type(type_type)
    result = assemble(input_file, output, chip, quiet, str(type_type))
    if result and exec:
        print_messages(quiet, 'EXEC', chip, '')
        did_execute = execute(chip, 'rom', 0, monitor, quiet,
                              chip.OPERATIONS)
        if did_execute:
            if results:
                quiet = False
            print_messages(quiet, 'BLANK', chip, '')
            print_messages(quiet, 'ACC', chip, '')
            print_messages(quiet, 'CARRY', chip, '')
            print_messages(quiet, 'BLANK', chip, '')
            # Display results
            if show != '':
                coredump(chip, '', str(show))


@cli.command()
@click.help_option('--help', '-h')
@click.option('--objectfile', '-o',
              help='4004 object or binary file (specify extension)',
              metavar='<filename>', type=str)
@click.option('--inst', '-i',
              help='Instuctions to disassemble',
              metavar='<Between 1 & 4096>',
              type=int)
@click.option('--labels', '-l',
              help='Show label table', type=bool,
              is_flag=True, default=False)
@click.option('--config', '-c', metavar='<filename>', type=str,
              help='Configuration file', default='')
def dis(objectfile: str, inst: int, labels: bool,
        config) -> None:
    """Disassemble the input file"""
    # Ensure that the core Pyntel4004 is installed
    # Exit if not
    if not is_core_installed(core_name):
        raise CoreNotInstalled(cini)
    object_file = objectfile
    if config != '':
        configuration = get_config(config)
        if "dis" in configuration:
            dis_configuration = configuration["dis"]
            object_file, inst, labels = check_dis_content(dis_configuration,
                                                          object_file, inst,
                                                          labels)
        else:
            raise click.BadOptionUsage(
                "--config", "No 'dis' section in configuration file\n")
    inst = check_inst(inst)
    # Create new instance of a processor
    chip = Processor()
    memory_space, _, lbls = retrieve(object_file, chip, False)
    disassemble(chip, memory_space, 0, inst, labels, lbls)


@cli.command()
@click.help_option('--help', '-h')
@click.option('--objectfile', '-o',
              help='4004 object or binary file (specify extension)',
              metavar='<filename>')
@click.option('--quiet', '-q', is_flag=True,
              help='Output on/off')
@click.option('--results', '-r', is_flag=True,
              help='Results on/off')
@click.option('--config', '-c', metavar='<filename>',
              help='Configuration file', default='')
def exe(objectfile, quiet, config, results):
    """Execute the object file"""
    # Ensure that the core Pyntel4004 is installed
    # Exit if not
    if not is_core_installed(core_name):
        raise CoreNotInstalled(cini)
    if config != '':
        configuration = get_config(config)
        show = check_results_content(configuration["results"])
        if "exe" in configuration:
            exe_configuration = configuration["exe"]
            if "objectfile" in exe_configuration and objectfile is None:
                objectfile = exe_configuration["objectfile"]
            quiet = check_quiet(quiet, exe_configuration)
        else:
            raise click.BadOptionUsage(
                "--config", "No 'exe' section in configuration file\n")
    else:
        show = "['ALL']"
    # Create new instance of a processor
    chip = Processor()
    result = retrieve(objectfile, chip, quiet)
    memory_space = result[0]
    did_execute = execute(chip, memory_space, 0, False, quiet, chip.OPERATIONS)
    print("here")
    if did_execute:
        if results:
            quiet = False
        print_messages(quiet, 'BLANK', chip, '')
        print_messages(quiet, 'ACC', chip, '')
        print_messages(quiet, 'CARRY', chip, '')
        print_messages(quiet, 'BLANK', chip, '')
        # Display results
        if show != '':
            coredump(chip, '', str(show))
