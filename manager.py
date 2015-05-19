import pydwarf
from raws import *
from settings import exportsettings as settings
from utils import copytree

# Actually run the program
def __main__():
    
    pydwarf.log.info('Running PyDwarf %s' % pydwarf.__version__)
    
    if os.path.exists(settings.rawsdir):
    
        if settings.backup and settings.backupdir:
            copytree(settings.rawsdir, settings.backupdir)
        else:
            pydwarf.log.warning('Proceeding without backing up raws.')
        
        pydwarf.log.info('Reading raws...')
        r = raws().read(dir=settings.rawsdir, verbose=False)
        
        pydwarf.log.info('Running scripts...')
        for script in settings.runscripts:
            
            scriptname = None
            scriptfunc = None
            scriptargs = None
            if isinstance(script, tuple) or isinstance(script, list):
                scriptargs = script[1]
                script = script[0]
            if callable(script):
                scriptname = script.__name__
                scriptfunc = script
            else:
                scriptname = script
                scriptfunc = pydwarf.urist.get(script)
            
            if scriptfunc:
                scriptinfo = 'Running script %s' % scriptname
                if scriptargs: scriptinfo = '%s with args %s' % (scriptinfo, scriptargs)
                pydwarf.log.info('%s...' % scriptinfo)
                
                try:
                    response = scriptfunc(r, **scriptargs) if scriptargs else scriptfunc(r)
                    success = response.get('success')
                    status = response['status'] if 'status' in response else ('Script ran %ssuccessfully' % ('' if success else 'un'))
                    pydwarf.log.info('%s: %s' % ('SUCCESS' if success else 'FAILURE', status))
                    
                except Exception:
                    pydwarf.log.exception('Unhandled exception while running script %s.' % scriptname)
                    
                else:
                    pydwarf.log.info('Finished running script %s.' % scriptname)
                    
            else:
                pydwarf.log.error('Failed to load script %s.' % scriptname)
        
        pydwarf.log.info('Writing changes to raws...')
        outputdir = settings.outputdir if settings.outputdir else settings.rawsdir
        if not os.path.exists(outputdir): os.makedirs(outputdir)
        r.write(outputdir, verbose=False)
        
        pydwarf.log.info('All done!')
        
    else:
        pydwarf.log.info('Specified raws directory does not exist.')

if __name__ == "__main__":
    __main__()
