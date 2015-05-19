import os
import traceback
from raws import raws
import settings
import scripts
import shutil

__version__ = 'alpha'

def __main__():
    
    print 'Running PyDwarf %s' % __version__
    
    if os.path.exists(settings.rawsdir):
    
        if settings.backup and settings.backupdir:
            copytree(settings.rawsdir, settings.backupdir)
        else:
            print 'WARNING: Proceeding without backing up raws.'
        
        print 'Reading raws...'
        r = raws().read(dir=settings.rawsdir, verbose=False)
        
        print 'Running scripts...'
        for script in settings.scripts:
            
            scriptname = script
            scriptargs = None
            if isinstance(script, tuple) or isinstance(script, list):
                scriptname = script[0]
                scriptargs = script[1]
                
            if scriptname in scripts.loaded:
                print 'Running script %s%s...' % (scriptname, (' with args %s' % scriptargs) if scriptargs else '')
                
                try:
                    if scriptargs:
                        response = scripts.loaded[scriptname](r, **scriptargs)
                    else:
                        response = scripts.loaded[scriptname](r)
                    
                    success = ('success' in response and response['success'])
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
        r.write(settings.outputdir if settings.outputdir else settings.rawsdir, verbose=False)
        
        print 'All done!'
        
    else:
        print 'Specified raws directory does not exist.'

# credit belongs to http://stackoverflow.com/a/13814557/3478907
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)
    
if __name__ == "__main__":
    __main__()
