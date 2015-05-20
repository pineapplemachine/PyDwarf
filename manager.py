import re
import pydwarf
from raws import *
from settings import exportsettings as settings
from utils import copytree

# Actually run the program
def __main__():
    
    pydwarf.log.info('Running PyDwarf %s.' % pydwarf.__version__)
    if settings.dfversion is not None:
        pydwarf.log.info('Managing Dwarf Fortress version %s.' % settings.dfversion)
    else:
        pydwarf.log.error('No Dwarf Fortress version was specified in settings. Scripts will be run regardless of their indicated compatibility.')
    
    if os.path.exists(settings.rawsdir):
    
        if settings.backup and settings.backupdir:
            pydwarf.log.info('Backing up raws to %s...' % settings.backupdir)
            copytree(settings.rawsdir, settings.backupdir)
        else:
            pydwarf.log.warning('Proceeding without backing up raws.')
        
        pydwarf.log.info('Reading raws from %s...' % settings.rawsdir)
        r = raws().read(settings.rawsdir, pydwarf.log)
        
        pydwarf.log.info('Running scripts...')
        for script in settings.runscripts:
            pydwarf.log.debug('Handling script %s...' % script)
            
            urist = None
            scriptname = None
            scriptfunc = None
            scriptargs = None
            if isinstance(script, tuple) or isinstance(script, list):
                scriptargs = script[1]
                script = script[0]
            elif isinstance(script, dict):
                scriptname = script.get('name')
                scriptargs = script.get('args')
                scriptmatch = script.get('match')
                candidates = pydwarf.urist.get(scriptname, version=settings.dfversion, match=scriptmatch)
                if candidates and len(candidates):
                    urist = candidates[0]
                    if len(candidates) > 1: pydwarf.log.warning('More than one fitting script has been specified, using a best guess.')                        
            elif callable(script):
                scriptname = script.__name__
                scriptfunc = script
            else:
                scriptname = script
                candidates = pydwarf.urist.get(scriptname, version=settings.dfversion)
                if candidates and len(candidates):
                    urist = candidates[0]
                    if len(candidates) > 1: pydwarf.log.warning('More than one fitting script has been specified, using a best guess.')
            if urist and scriptfunc is None:
                scriptfunc = urist.fn
            
            if scriptfunc:
                scriptinfo = 'Running script %s' % scriptname
                if scriptargs: scriptinfo = '%s with args %s' % (scriptinfo, scriptargs)
                pydwarf.log.info('%s...' % scriptinfo)
                
                try:
                    response = scriptfunc(r, **scriptargs) if scriptargs else scriptfunc(r)
                    success = response.get('success')
                    status = response['status'] if 'status' in response else ('Script %s ran %ssuccessfully.' % (scriptname, '' if success else 'un'))
                    pydwarf.log.info('%s: %s' % ('SUCCESS' if success else 'FAILURE', status))
                except Exception:
                    pydwarf.log.exception('Unhandled exception while running script %s.' % scriptname)
                else:
                    pydwarf.log.info('Finished running script %s.' % scriptname)

            else:
                pydwarf.log.error('Failed to retrieve script %s.' % scriptname)
        
        outputdir = settings.outputdir if settings.outputdir else settings.rawsdir
        pydwarf.log.info('Writing changes to raws to %s...' % outputdir)
        if not os.path.exists(outputdir): os.makedirs(outputdir)
        r.write(outputdir, pydwarf.log)
        
        pydwarf.log.info('All done!')
        
    else:
        pydwarf.log.info('Specified raws directory does not exist.')

if __name__ == "__main__":
    __main__()
