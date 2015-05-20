import pydwarf
from raws import *
from settings import exportsettings as settings
from utils import copytree

# Actually run the program
def __main__():
    
    pydwarf.log.info('Running PyDwarf %s' % pydwarf.__version__)
    
    if os.path.exists(settings.rawsdir):
    
        if settings.backup and settings.backupdir:
            pydwarf.log.info('Backing up raws to %s...' % settings.backupdir)
            copytree(settings.rawsdir, settings.backupdir)
        else:
            pydwarf.log.warning('Proceeding without backing up raws.')
        
        pydwarf.log.info('Reading raws from %s...' % settings.rawsdir)
        r = raws().read(dir=settings.rawsdir, verbose=False)
        
        pydwarf.log.info('Running scripts...')
        for script in settings.runscripts:
            pydwarf.log.debug('Handling script %s...' % script)
            
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
                funcs = pydwarf.urist.get(scriptname)
                if funcs and len(funcs):
                    if scriptmatch:
                        matchfuncs = []
                        for func in funcs:
                            if all([func.metadata[i] == j for i, j in scriptmatch.iteritems()]): matchfuncs.append(func)
                        if len(matchfuncs):
                            scriptfunc = matchfuncs[-1].fn
                            if len(matchfuncs) > 1: 
                                pydwarf.log.warning('More than one script has been specified with the name %s and matching %s, using the most recently registered.' % scriptname, scriptmatch)
                        else:
                            pydwarf.log.error('Found no script by name %s and matching %s.' % (scriptname, scriptmatch))
                        
                    else:
                        scriptfunc = funcs[-1].fn
                    if len(funcs) > 1: 
                        pydwarf.log.warning('More than one script has been specified with the name %s, using the most recently registered.' % scriptname)
            elif callable(script):
                scriptname = script.__name__
                scriptfunc = script
            else:
                scriptname = script
                funcs = pydwarf.urist.get(scriptname)
                if funcs and len(funcs):
                    scriptfunc = funcs[-1].fn
                    if len(funcs) > 1: 
                        pydwarf.log.warning('More than one script has been specified with the name %s, using the most recently registered.' % scriptname)
            
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
                pydwarf.log.error('Failed to load script %s.' % scriptname)
        
        outputdir = settings.outputdir if settings.outputdir else settings.rawsdir
        pydwarf.log.info('Writing changes to raws to %s...' % outputdir)
        if not os.path.exists(outputdir): os.makedirs(outputdir)
        r.write(outputdir, verbose=False)
        
        pydwarf.log.info('All done!')
        
    else:
        pydwarf.log.info('Specified raws directory does not exist.')

if __name__ == "__main__":
    __main__()
