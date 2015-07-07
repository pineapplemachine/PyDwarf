#!/usr/bin/env python

__author__ = 'Sophie Kirschner'
__license__ = 'zlib/libpng'
__email__ = 'sophiek@pineapplemachine.com'
__version__ = '1.0.1'



import re
import os
import shutil
import json
import argparse
import importlib
import pydwarf
import raws



jsonconfigpath = 'config.json'



# Actually run the program
def __main__(args=None):
    conf = getconf(args)
    pydwarf.log.debug('Proceeding with configuration: %s.' % conf)
    
    # Report versions
    pydwarf.log.info('Running PyDwarf manager version %s.' % __version__)
    pydwarf.log.debug('With pydwarf version %s.' % pydwarf.__version__)
    pydwarf.log.debug('With raws version %s.' % raws.__version__)
    pydwarf.log.debug('With Dwarf Fortress version %s.' % conf.version)
    pydwarf.log.debug('With DFHack version %s.' % conf.hackversion)
    
    # Handle flags that completely change behavior
    specialtext = None
    
    if args.list:
        items = pydwarf.urist.list()
        specialtext = '\n'.join(items)
    elif args.meta is not None:
        specialtext = pydwarf.urist.doclist(args.meta, format=args.metaformat)
    
    if specialtext is not None:
        pydwarf.log.info('\n\n%s\n' % specialtext)
        if args.writedoc:
            with open(args.writedoc, 'wb') as writedoc: writedoc.write(specialtext)
        exit(0)
    
    # Verify that input directory exists
    if not os.path.exists(conf.input):
        pydwarf.log.error('Specified raws directory %s does not exist.' % conf.input)
        exit(1)
    
    # Create a new session
    pydwarf.log.info('Configuring session using raws input directory %s.' % conf.input)
    session = pydwarf.session(raws, conf)
    
    # Make backup
    if conf.backup is not None:
        pydwarf.log.info('Backing up raws to directory %s.' % conf.backup)
        session.backup()
    else:
        pydwarf.log.warning('Proceeding without backing up raws.')
    
    # Run each script
    pydwarf.log.info('Running scripts.')
    session.handleall()
    
    # Write the output
    outputdir = conf.output if conf.output else conf.input
    pydwarf.log.info('Writing new raws to directory %s.' % outputdir)
    session.write(outputdir)
    
    # All done!
    pydwarf.log.info('All done!')



def getconf(args=None):
    # Load initial config from json file
    conf = pydwarf.config()
    if os.path.isfile(jsonconfigpath): conf.json(jsonconfigpath)
    
    # Default name of configuration override package
    overridename = 'config_override'
    
    # Override settings from command line arguments, first check for --config argument
    if args.config:
        if args.config.endswith('.json'):
            conf.json(args.config)
        else:
            overridename = args.config
    
    # Apply settings in override package
    overrideexception = None
    if overridename and (os.path.isfile(overridename + '.py') or os.path.isfile(os.path.join(overridename, '__init__.py'))):
        try:
            package = importlib.import_module(overridename)
            conf.apply(package.export)
        except Exception, e:
            overrideexception = e
            
    # Apply other command line arguments   
    conf.apply(args.__dict__)
    
    # Setup logger
    conf.setuplogger()
    
    # If there was an exception when reading the overridename package, report it now
    # Don't report it earlier because the logger wasn't set up yet
    if overrideexception:
        pydwarf.log.error('Failed to apply configuration from %s package.\n%s' % (overridename, overrideexception))
        
    # Handle things like automatic version detection, package importing
    conf.setup()
    
    # All done!
    return conf



def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ver', '--version', help='indicate Dwarf Fortress version', type=str)
    parser.add_argument('-i', '--input', help='raws input directory', type=str)
    parser.add_argument('-o', '--output', help='raws output directory', type=str)
    parser.add_argument('-b', '--backup', help='raws backup directory', type=str)
    parser.add_argument('-t', '--paths', help='which paths relative to input to store in memory and allow access to', nargs='+', type=str)
    parser.add_argument('-s', '--scripts', help='run scripts by name or namespace', nargs='+', type=str)
    parser.add_argument('-p', '--packages', help='import packages containing PyDwarf scripts', nargs='+', type=str)
    parser.add_argument('-c', '--config', help='run with json config file if the extension is json, otherwise treat as a Python package, import, and override settings using export dict', type=str)
    parser.add_argument('-v', '--verbose', help='set stdout logging level to DEBUG', action='store_true')
    parser.add_argument('-hver', '--hackversion', help='indicate DFHack version', type=str)
    parser.add_argument('--log', help='output log file to path', type=str)
    parser.add_argument('--list', help='list available scripts', action='store_true')
    parser.add_argument('--jscripts', help='specify scripts given a json array', type=str)
    parser.add_argument('--meta', help='show metadata for scripts', nargs='*', type=str)
    parser.add_argument('--metaformat', help='how to format shown metadata', type=str)
    parser.add_argument('--writedoc', help='write data given by --list or --meta to a file path in addition to the log', type=str)
    args = parser.parse_args()
    
    if args.jscripts is not None: args.scripts = json.loads(args.jscripts) if args.scripts is None else (args.scripts + json.loads(args.jscripts))
    
    return args



if __name__ == "__main__":
    __main__(parseargs())
