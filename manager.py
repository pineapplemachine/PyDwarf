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
        successfulscripts = []
        for script in settings.runscripts:
            pydwarf.log.debug('Handling script %s...' % script)
            
            urist, scriptname, scriptfunc, scriptargs, scriptmatch = getscriptinfo(script)
            
            if scriptfunc:
                if checkdependencies(urist, successfulscripts):
                    scriptinfo = 'Running script %s' % scriptname
                    if scriptargs: scriptinfo = '%s with args %s' % (scriptinfo, scriptargs)
                    pydwarf.log.info('%s...' % scriptinfo)
                    
                    try:
                        response = scriptfunc(r, **scriptargs) if scriptargs else scriptfunc(r)
                        if response:
                            success = response.get('success')
                            status = response['status'] if 'status' in response else ('Script %s ran %ssuccessfully.' % (scriptname, '' if success else 'un'))
                            pydwarf.log.info('%s: %s' % ('SUCCESS' if success else 'FAILURE', status))
                            if success and urist is not None:
                                successfulscripts.append(urist)
                        else:
                            pydwarf.log.error('Received no response from script %s.' % scriptname)
                    except Exception:
                        pydwarf.log.exception('Unhandled exception while running script %s.' % scriptname)
                    else:
                        pydwarf.log.info('Finished running script %s.' % scriptname)
                        
                else:
                    pydwarf.log.error('Dependencies %s not met for script %s.' % (urist.meta('dependency'), scriptname))

            else:
                pydwarf.log.error('Failed to retrieve script %s.' % scriptname)
        
        outputdir = settings.outputdir if settings.outputdir else settings.rawsdir
        if os.path.exists(outputdir):
            pydwarf.log.info('Removing obsolete raws from %s...' % outputdir)
            for removefile in [os.path.join(outputdir, f) for f in os.listdir(outputdir)]:
                pydwarf.log.debug('Removing file %s...' % removefile)
                if removefile.endswith('.txt'): os.remove(removefile)
        else:
            pydwarf.log.info('Creating raws output directory %s...' % outputdir)
            os.makedirs(outputdir)
            
        pydwarf.log.info('Writing changes to raws to %s...' % outputdir)
        r.write(outputdir, pydwarf.log)
        
        pydwarf.log.info('All done!')
        
    else:
        pydwarf.log.info('Specified raws directory does not exist.')

def getscriptinfo(script):
    # A script can be specified in a variety of ways in the scripts iterable, this function is for understanding all the different options and returning the info the manager needs.
    
    urist = None
    scriptname = None
    scriptfunc = None
    scriptargs = None
    scriptmatch = None
    scriptignoreversion = None
    checkversion = settings.dfversion
    
    if isinstance(script, pydwarf.urist):
        urist = script
        
    elif callable(script):
        scriptfunc = script
        urist = pydwarf.urist.forfunc(scriptfunc)
    
    elif isinstance(script, basestring):
        scriptname = script
                
    elif isinstance(script, dict):
        scriptname = script.get('name')
        scriptfunc = script.get('func')
        scriptargs = script.get('args')
        scriptmatch = script.get('match')
        scriptignoreversion = script.get('ignore_df_version')
        
    if scriptignoreversion:
        checkversion = None
        
    if urist is None and scriptname is not None:
        candidates = pydwarf.urist.get(scriptname, version=checkversion, match=scriptmatch)
        if candidates and len(candidates):
            urist = candidates[0]
            if len(candidates) > 1: pydwarf.log.error('More than one fitting script has been specified, using a best guess.')
        
    if urist is not None:
        scriptname = urist.name
        scriptfunc = urist.fn
        
    if scriptname is None and scriptfunc is not None:
        scriptname = scriptfunc.__name__
        
    return urist, scriptname, scriptfunc, scriptargs, scriptmatch
    
def checkdependencies(urist, successfulscripts):
    if urist:
        deps = urist.meta('dependency')
        if deps is not None:
            # Allow single dependencies to be indicated without being inside an iterable
            if isinstance(deps, basestring) or isinstance(deps, dict): deps = (deps,)
            # Check each dependency
            depssatisfied = 0
            for dep in deps:
                pydwarf.log.debug('Checking for dependency %s...' % dep)
                urist, scriptname, scriptfunc, scriptargs, scriptmatch = getscriptinfo(dep)
                name, namespace = pydwarf.urist.splitname(scriptname)
                for script in successfulscripts:
                    if script.name == name and (namespace is None or script.meta('namespace') == namespace) and script.matches(scriptmatch):
                        depssatisfied += 1
                        break
            return depssatisfied == len(deps)
    return True

if __name__ == "__main__":
    __main__()

