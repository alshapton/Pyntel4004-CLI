.. _cli:

.. include:: global.rst

Basic Usage
-----------

`4004 <command> <options> <arguments>`

`<command>`

 - `asm`  Assemble the input file
 - `dis`  Disassemble the input file
 - `exe`  Execute the object file

`<options>`

 - **-h**, **- -help**: Show help.
 - **-v**, **- -version**:  Show the version and exit.

``asm`` options:

 - **-i**, **- -input** `<input file>`: assembly language source file.
 - **-o**, **- -output** `<output file>`: object code output file.
 - **-e**, **- -exec**: execute the assembled program if successful assembly.
 - **-t**, **- -type** `<extension>`: Type of output required. (multiple output types can be specified)
     
     - `bin` will deliver a binary file of machine code
     
     - `obj` will deliver an object module which can be loaded back into the disassembler for debugging

     - `h` will deliver a c-style header file that can be used in a RetroShield Arduino to run the code on a real 4004

     - `ALL` will deliver all of the above

    .. collapse:: Changelog
        
        New in 0.0.1-alpha.2
 - **-c**, **- -config** `<config file>`: use the specified config file
 
    .. collapse:: Changelog
        
        New in 0.0.1-alpha.2
 - **-q**, **- -quiet**: Quiet mode on x
 - **-m**, **- -monitor**: Start monitor x

 - **-h**, **- -help**: Show help.

x Mutually exclusive parameters

``dis`` options.

- **-o**, **- -object** `<object file>`: object code or binary input file.

- **-l**, **- -labels**: show the label table (only available in .OBJ files)

    .. collapse:: Changelog
        
        New in 0.0.1-alpha.2
- **-c**, **- -config** `<config file>`: use the specified config file

    .. collapse:: Changelog
        
        New in 0.0.1-alpha.2
- **-b**, **- -inst**: number of instructions to disassemble (between 1 and 4096).
- **-h**, **- -help**: Show help.

    *It is the user's responsibility to understand that if a byte count causes the disassembler to end up midway through a 2-byte instruction, that last instruction will not be disassembled correctly.*


``exe`` options.

- **-o**, **- -object** `<object file>`: object code or binary input file.
- **-c**, **- -config** `<config file>`: use the specified config file

    .. collapse:: Changelog
        
        New in 0.0.1-alpha.2
- **-q**, **- -quiet**: Quiet mode on

- **-h**, **- -help**: Show help.


Error Messages
--------------

Error messages are displayed when there are issues with either the supplied command, or issues with the source code itself. The errors are raised as exceptions, with an exception type together with an information message

.. list-table:: Errors
   :widths: 10 30 20 40
   :header-rows: 1

   * - Command
     - Exception
     - Options
     - Message
   * - asm
     - BadParameter
     - 
     - Invalid Parameter Combination: |br| --quiet and --monitor cannot be used |br| together
   * - asm
     - BadOptionUsage
     - \--type
     - Invalid output type specified
   * - asm
     - BadOptionUsage
     - \--type
     - Cannot specify 'ALL' with any others
   * - dis
     - BadOptionUsage
     - \--inst
     - Instructions should be between 1 |br| and 4096
   * - ALL
     - ConfigFileNotFound
     - \--config
     - Configuration file not found.


.. list-table:: Special Error Message
   :widths: 20 80
   :header-rows: 1

   * - Exception
     - Message
   * - CoreNotInstalled
     - Pyntel4004 core is not installed - use pip install Pyntel4004


Configuration Files
-------------------
    .. collapse:: Changelog
        
        New in 0.0.1-alpha.2

Pyntel4004-cli configuration files are specified using the `TOML <http://toml.io>`_ notation. This is a notation which favours humans over machines, so it is easy to understand and write the configuration you want.

Example Configuration File - example2.toml

.. code-block:: toml

    # Configuration for Pyntel4004-cli.

    title = "Configuration file for example2.asm"

    [asm]
    input = "example2.asm"
    output = "example2"
    type = ["BIN", "H"]
    exec = true
    monitor = true
    quiet = true

    [dis]
    object = "examples/example2.obj"
    inst = 6
    labels = true

    [exe]
    object = "examples/example2.obj"
    quiet = true


The configuration file has 4 sections:

This MUST be first

i)    The title - simply a description of what the configuration file is for. Note that any comments (lines starting with a ``#`` can be added anywhere for readability).

(in no particular order)

ii)  ``[asm]`` section containing directives for the assembly of a specific program source file

iii) ``[dis]`` section containing directives for the disassembly of a specific object module

iv)  ``[exe]`` section containing directives for the execution of a specific object module

The valid configuration tokens are shown in the example above - they mirror the options that can be specified on the command line. 

ANY of the configuration tokens can be overriden simply by specifying them on the command line.
