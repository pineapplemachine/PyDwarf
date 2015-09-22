# Map of PyDwarf's file structure

- **PyDwarf**  
  This is the root directory and everything else is inside it.
  
  - **docs** (You are here!)  
    This directory contains documentation and scripts for automatically building or otherwise fucking around with documentation.
    
    - **bin**  
      Contains stuff like a script to make html documentation from PyDwarf's docstrings, a script to generate a markdown file containing descriptions of each script registered with PyDwarf, and a script which actually runs those examples in `docs/examples/` to make sure all of them work like they're supposed to.
      
    - **config**  
      Here you can find examples of PyDwarf configuration files in formats other than yaml.
      
    - **examples**  
      This is where files containing various code examples and their outputs reside. Someday these examples will be automagically used in generated html documentation.
      
  - **images**  
    Here are some images somehow related to PyDwarf, such as logos and a favicon.
    
  - **lib**  
    PyDwarf uses some packages that aren't part of Python's standard libary. This is where those packages reside, because installing them on-demand would be hard.
    
  - **logs**  
    Where log files will end up when PyDwarf starts generating them. (And it makes a lot of log files! If you're running PyDwarf frequently you might want to go in here and clean things up by deleting old logs every now and then.)
    
  - **pydwarf**  
    PyDwarf relies on two packages written specifically for it, and this one is where code for loading configurations and registering scripts and running them and stuff of that nature makes its home.
    
  - **raws**  
    This is the other package, and this one is for stuff like loading a Dwarf Fortress directory, parsing the files in it, and making them easily accessible to other scripts. Think of your Dwarf Fortress directory as a line drawing and the raws package as your crayons.
    
  - **scripts**  
    Here's where PyDwarf looks for mods by default. Mods take the form of Python scripts with special names and function decorators that help PyDwarf know which files it needs to load and which ones aren't its business. This directory contains loads of subdirectories, each of which represents a different mod author and contains scripts for applying the mods they made.
