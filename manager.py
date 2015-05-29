import re
import os
import pydwarf
import raws
import config
from utils import copytree

# Actually run the program
def __main__():
    
    # Get configuration
    conf = config.export
    if not conf:
        pydwarf.log.error('No configuration specified. Imported config package must contain an export variable.')
        exit(1)
    
    # Things to do with versions
    pydwarf.log.info('Running PyDwarf %s.' % pydwarf.__version__)
    if conf.version is not None:
        pydwarf.log.info('Managing Dwarf Fortress version %s.' % conf.version)
        pydwarf.urist.session.dfversion = conf.version
    else:
        pydwarf.log.error('No Dwarf Fortress version was specified in conf. Scripts will be run regardless of their indicated compatibility.')
    
    # Verify that input directory exists
    if not os.path.exists(conf.input):
        pydwarf.log.error('Specified raws directory %s does not exist.' % conf.input)
        exit(1)
    
    # Make backup
    if conf.backup is not None:
        pydwarf.log.info('Backing up raws to %s...' % conf.backup)
        try:
            copytree(conf.input, conf.backup)
        except:
            pydwarf.log.error('Failed to create backup.')
            exit(1)
    else:
        pydwarf.log.warning('Proceeding without backing up raws.')
    
    # Read input raws
    pydwarf.log.info('Reading raws from input directory %s...' % conf.input)
    pydwarf.urist.session.dfraws = raws.dir(path=conf.input, log=pydwarf.log)
    
    # Run each script
    pydwarf.log.info('Running scripts...')
    pydwarf.urist.session.handleall(conf.scripts)
    
    # Get the output directory, remove old raws if present
    outputdir = conf.output if conf.output else conf.input
    if os.path.exists(outputdir):
        pydwarf.log.info('Removing obsolete raws from %s...' % outputdir)
        for removefile in [os.path.join(outputdir, f) for f in os.listdir(outputdir)]:
            pydwarf.log.debug('Removing file %s...' % removefile)
            if removefile.endswith('.txt'): os.remove(removefile)
    else:
        pydwarf.log.info('Creating raws output directory %s...' % outputdir)
        os.makedirs(outputdir)
    
    # Write the output
    pydwarf.log.info('Writing changes to raws to %s...' % outputdir)
    pydwarf.urist.session.dfraws.write(outputdir, pydwarf.log)
    
    # All done!
    pydwarf.log.info('All done!')



if __name__ == "__main__":
    __main__()
