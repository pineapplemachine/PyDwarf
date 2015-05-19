PyDwarf has several very important files:

manager.py is where the magic happens. Screw around in settings.py before running it, then watch it make all sorts of changes to your raws.

pydwarf.py contains resources that should be used by scripts which are intended to be managed by pydwarf.

raws.py contains classes and methods that allow for flexible querying of DF's raws. Tokens can be searched for and modified. raws.py imposes no implicit structure upon the files it parses and so it may sometimes be necessary to construe more complicated queries to ensure the tokens you're looking at are exactly the ones you mean to.

settings.py sets some variables that are used to tell PyDwarf where to find raws, where to put the modified ones, and where to back up the originals, which scripts to run, in which order, and with what arguments. Lots of cool stuff. Scripts should always be located in the scripts/ directory underneath PyDwarf's root directory. Names specified in the list of scripts correspond to functions defined in any file within that directory, and any arguments specified here are passed via **kwargs. The first argument to those functions represents the raws object which can be queried and modified.

Please look at the scripts within the scripts/ directory for examples of how to work with PyDwarf.
