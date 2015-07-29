# PyDwarf via the command line

## Introduction

Running PyDwarf using settings in `config` files is straightforward: When `python manager.py` is executed, files like `config.yaml` or `config.py` are looked for in PyDwarf's root directory. However, there may be cases when it's desireable to run PyDwarf from the command line with a certain configuration without editing configuration files. Note that this is an advanced feature and the vast majority of users should never have to worry about these command line arguments. These are implemented primarily as a way to make it easier for other applications to call on PyDwarf for some of the heavy lifting.

![Example gif of running PyDwarf from the command line](http://www.pineapplemachine.com/pydwarf/terminal_example.gif)

## Accepted arguments

There is a 1:1 mapping of long argument names to the values in configuration files. For a more verbose explanation of the purpose each argument serves it would be best to look to [TODO](config.md).

* `-i` `--input`: DF input directory. Expects a directory path.
* `-o` `--output`: DF output directory. Expects a directory path.
* `-bak` `--backup`: DF backup directory. Expects a directory path.
* `-p` `--paths`: Important DF paths. Expects one or more paths relative to DF root.
* `-ver` `--version`: Indiciate DF version. Set to `auto` for automatic detection.
* `-hver` `--hackversion`: Indicate DFHack version. Set to `auto` for automatic detection.
* `-l` `-log`: Path to log file output. Expects a file path.
* `-v` `--verbose`: Sets stdout logging level to DEBUG.
* `-s` `--scripts`: One or more names of scripts to run.
* `-js` `--jscripts`: A list of scripts to run given in json format.
* `-pk` `--packages`: A list of Python packages to import.
* `-c` `--config`: Paths to one or more config files to load. Later configs override prior ones.
* `-ls` `--list`: List registered scripts with current configuration.
* `-m` `--meta`: Show documentation for script names given, or all scripts if no name is given.
* `-mf` `--metaformat`: How to format metadata shown by `--meta`. Accepts `txt`, `html`, `md`.
* `-wd` `--writedoc`: Write information outputted by `--meta` or `--list` to a file path.
* `-h` `--help`: Display a summary of each argument's purpose.
