# Pyntel4004-cli

![Pyntel4004-cli Logo](https://raw.githubusercontent.com/alshapton/Pyntel4004-cli/main/images/pyntel4004-cli.png)

[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=alshapton_Pyntel4004-cli)

<h1>Command Line Interface for Pyntel4004</h1>

### Basic Usage.###

`4004 <command> <options> <arguments>`

`<command>`
- `asm`  Assemble the input file
- `dis`  Disassemble the input file
- `exe`  Execute the object file

`<options>`
- **-h**, **--help**: Show help.
- **-v**, **--version**:  Show the version and exit.

<br>
<br>

#### `asm` options.

- **-i**, **--input** `<input file>`: assembly language source file [required].
- **-o**, **--output** `<output file>`: object code output file.
- **-e**, **--exec**: execute the assembled program if successful assembly.
- **-t**, **--type** `<extension>`: Multiple output types can be specified - (bin/obj/h or ALL)
    - `bin` will deliver a binary file of machine code
    
    - `obj` will deliver an object module which can be loaded back into the disassembler for debugging

    - `h` will deliver a c-style header file that can be used in a RetroShield Arduino to run the code on a real 4004

    - `ALL` will deliver all of the above<details>New in 0.0.1-alpha2<summary>Changelog</summary></details>
- **-q**, **--quiet**: Quiet mode on *
- **-m**, **--monitor**: Start monitor*

- **-h**, **--help**: Show help.

*Mutually exclusive parameters

<br>
<br>

#### `dis` options.

- **-o**, **--object** `<object file>`: object code or binary input file. [required]

- **-l**, **--labels**: show the label table (only available in .OBJ files)<details>New in 0.0.1-alpha2<summary>Changelog</summary></details>

- **-b**, **--byte**: number of bytes to disassemble (between 1 and 4096).
- **-h**, **--help**: Show help.

    *It is the user's responsibility to understand that if a byte count causes the disassembler to end up midway through a 2-byte instruction, that last instruction will not be disassembled correctly.*

<br>
<br>

#### `exe` options.

- **-o**, **--object** `<object file>`: object code or binary input file.[required].
- **-q**, **--quiet**: Quiet mode on

- **-h**, **--help**: Show help.
