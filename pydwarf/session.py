#!/usr/bin/env python
# coding: utf-8

import os
import shutil

from urist import urist
from uristscript import uristscript
from logger import log
from config import config



class session(object):
    '''
        Class contains functionality for abstract handling for scripts and dirs.
    '''
    
    def __init__(self, raws=None, conf=None):
        '''Initialize a session object.'''
        self.df = None
        self.dfversion = None
        self.conf = None
        self.raws = None
        self.successes = []
        self.failures = []
        self.noresponse = []
        if raws is not None and conf is not None: self.configure(raws, conf)
        
    def configure(self, raws, conf):
        '''
            Configure a session object given a reference to the raws package and
            to a configuration object.
        '''
        self.raws = raws
        self.conf = conf
        self.dfversion = conf.version
        if conf.input and os.path.isdir(conf.input):
            self.df = raws.dir(root=conf.input, dest=conf.output, paths=conf.paths, version=conf.version, log=log)
        else:
            log.error('Specified input directory %s does not exist.' % conf.input)
            
    def __enter__(self):
        '''Support for with/as syntax.'''
        if self.conf.backup: self.backup()
        return self
    def __exit__(self, type, value, traceback):
        '''Support for with/as syntax.'''
        if traceback is None: self.write(self.outputdir())
            
    def load(self, raws, *args, **kwargs):
        '''
            Configure a session object given arguments to specify configuration
            loading behavior.
        '''
        self.configure(raws, config.load(*args, **kwargs))
            
    def run(self):
        '''
            Backup the session's Dwarf Fortress directory, run specified
            scripts, and then write the output.
        '''
        if self.conf is None: raise ValueError('Failed to run session because it doesn\'t have a configuration object.')
        
        # Backup
        if self.conf.backup:
            self.backup()
        else:
            log.warning('Proceeding without first backing up raws.')
            
        # Run scripts
        self.handleall()
        
        # Write output
        self.write(self.outputdir())
        
    def outputdir(self):
        '''Get output directory given the session's configuration.'''
        return self.conf.output if self.conf.output else self.conf.input
    
    def successful(self, info):
        '''Get a list of successfully run scripts.'''
        return self.inlist(info, self.successes)
    def failed(self, info):
        '''Get a list of unsuccessfully run scripts.'''
        return self.inlist(info, self.failures)
        
    def inlist(self, info, flist):
        '''Internal: Get scripts in a given list.'''
        funcs = self.funcs(info)
        if funcs:
            return any([(func in flist) for func in funcs])
        else:
            return False
        
    def eval(self, func, args=None):
        '''Evaluate an uristscript or other callable object.'''
        
        # If the function is actually an urist, make sure we know that
        uristinstance = None
        if isinstance(func, uristscript): 
            uristinstance = func
            func = uristinstance.func
            name = uristinstance.getname()
        else:
            name = func.__name__
        
        # Actually execute the script
        log.info('Running script %s%s.' % (name, ('with args %s' % args) if args else ''))
        try:
            response = func(self.df, **args) if args else func(self.df) # Call the function
            if response is not None:
                # Handle success/failure response
                log.info(str(response))
                (self.successes if response.success else self.failures).append(uristinstance if uristinstance else func)
            else:
                log.error('Received no response from script %s.' % name)
                self.noresponse.append(uristinstance if uristinstance else func)
            
        except Exception:
            log.exception('Unhandled exception while running script %s.' % name)
            return False
        
        else:
            return True
    
    def funcs(self, info):
        '''
            Get function information associated with an entry in a configuration
            object's scripts attribute.
        '''
        uristinstance, scriptname, scriptfunc, scriptargs, scriptmatch, checkversion = urist.info(info, self.dfversion)
        if uristinstance is None and scriptfunc is None and scriptname is not None:
            candidates, original, culled = urist.get(scriptname, version=checkversion, match=scriptmatch, session=self)
            if len(candidates):
                return candidates
            elif len(original):
                log.info('All of candidates %s were culled.' % [c.getname() for c in original])
                for reason, culled in culled.iteritems():
                    if len(culled): log.info('Candidates %s were culled for reason: %s' % ([c.getname() for c in culled], reason))
                return None
        elif uristinstance is not None:
            return (uristinstance,)
        elif scriptfunc is not None:
            return (scriptfunc,)
        else:
            return None
    
    def handle(self, info):
        '''Handle a single script.'''
        funcs = self.funcs(info)
        if funcs:
            for func in funcs: self.eval(func)
        else:
            log.error('Found no scripts matching %s.' % info)
            
    def handleall(self, infos=None):
        '''Handle all scripts specified by the session's configuration.'''
        if infos is None and self.conf is not None: infos = self.conf.scripts
        if infos and len(infos):
            for info in infos: self.handle(info)
        else:
            log.error('No scripts to run.')
            
    def write(self, dest=None, *args, **kwargs):
        '''Write the session's directory to its output path.'''
        log.info('Writing output to destination %s.' % dest)
        self.df.clean(dest=dest)
        self.df.write(dest=dest, *args, **kwargs)
        
    def backup(self, dest=None, skipfails=False):
        '''Backup inputted Dwarf Fortress directory.'''
        if dest is None: dest = self.conf.backup
        if not dest: raise ValueError('Failed to backup files because no destination was provided.')
        
        log.info('Backing up raws to desination %s.' % dest)
        for path in self.conf.paths:
            srcpath = os.path.join(self.conf.input, path)
            destpath = os.path.join(dest, path)
            
            if not os.path.isdir(os.path.dirname(destpath)): os.makedirs(os.path.dirname(destpath))
            
            if os.path.isfile(srcpath):
                shutil.copy2(srcpath, destpath)
            elif os.path.isdir(srcpath):
                self.raws.copytree(srcpath, destpath)
            elif skipfails:
                raise ValueError('Failed to backup path %s because it refers to neither a file nor a directory.' % srcpath)
