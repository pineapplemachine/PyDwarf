import pydwarf
from raws import *
import settings
from utils import copytree

# Actually run the program
def __main__():
    
    print 'Running PyDwarf %s' % pydwarf.__version__
    
    if os.path.exists(settings.rawsdir):
    
        if settings.backup and settings.backupdir:
            copytree(settings.rawsdir, settings.backupdir)
        else:
            print 'WARNING: Proceeding without backing up raws.'
        
        print 'Reading raws...'
        r = raws().read(dir=settings.rawsdir, verbose=False)
        
        print 'Running scripts...'
        for script in settings.runscripts:
            
            scriptname = None
            scriptfunc = None
            scriptargs = None
            if isinstance(script, tuple) or isinstance(script, list):
                script = script[0]
                scriptargs = script[1]
            if callable(script):
                scriptname = script.__name__
                scriptfunc = script
            else:
                scriptname = script
                scriptfunc = pydwarf.urist.get(script)
            
            if scriptfunc:
                print 'Running script %s%s...' % (scriptname, (' with args %s' % scriptargs) if scriptargs else '')
                
                try:
                    response = scriptfunc(r, **scriptargs) if scriptargs else scriptfunc(r)
                    success = response.get('success')
                    status = response['status'] if 'status' in response else ('Script ran %ssuccessfully' % ('' if success else 'un'))
                    print '%s: %s' % ('SUCCESS' if success else 'FAILURE', status)
                    
                except Exception:
                    print 'WARNING: Unhandled exception while running script %s.' % scriptname
                    traceback.print_exc()
                    
                else:
                    print 'Finished running script %s.' % scriptname
                    
            else:
                print 'WARNING: Failed to load script %s.' % scriptname
        
        print 'Writing changes to raws...'
        outputdir = settings.outputdir if settings.outputdir else settings.rawsdir
        if not os.path.exists(outputdir): os.makedirs(outputdir)
        r.write(outputdir, verbose=False)
        
        print 'All done!'
        
    else:
        print 'Specified raws directory does not exist.'

if __name__ == "__main__":
    __main__()
