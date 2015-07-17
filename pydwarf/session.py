#!/usr/bin/env python
# coding: utf-8

import os
import shutil

from urist import urist
from logger import log
from config import config



class session:
    def __init__(self, raws=None, conf=None):
        self.df = None
        self.dfversion = None
        self.conf = None
        self.raws = None
        self.successes = []
        self.failures = []
        self.noresponse = []
        if raws is not None and conf is not None: self.configure(raws, conf)
        
    def configure(self, raws, conf):
        self.raws = raws
        self.conf = conf
        self.dfversion = conf.version
        if conf.input and os.path.isdir(conf.input):
            self.df = raws.dir(root=conf.input, dest=conf.output, paths=conf.paths, version=conf.version, log=log)
        else:
            log.error('Specified input directory %s does not exist.' % conf.input)
            
    def load(self, raws, *args, **kwargs):
        self.configure(raws, config.load(*args, **kwargs))
            
    def run(self):
        if self.conf is None: raise ValueError('Failed to run session because it doesn\'t have a configuration object.')
        
        # Backup
        if self.conf.backup:
            self.backup()
        else:
            log.warning('Proceeding without first backing up raws.')
            
        # Run scripts
        self.handleall()
        
        # Write output
        outputdir = self.conf.output if self.conf.output else self.conf.input
        self.write(outputdir)
    
    def successful(self, info):
        return self.inlist(info, self.successes)
    def failed(self, info):
        return self.inlist(info, self.failures)
        
    def inlist(self, info, flist):
        funcs = self.funcs(info)
        if funcs:
            return any([(func in flist) for func in funcs])
        else:
            return False
        
    def eval(self, func, args=None):
        # If the function is actually an urist, make sure we know that
        uristinstance = None
        if isinstance(func, urist): 
            uristinstance = func
            func = uristinstance.fn
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
        funcs = self.funcs(info)
        if funcs:
            for func in funcs: self.eval(func)
        else:
            log.error('Found no scripts matching %s.' % info)
            
    def handleall(self, infos=None):
        if infos is None and self.conf is not None: infos = self.conf.scripts
        if infos and len(infos):
            for info in infos: self.handle(info)
        else:
            log.error('No scripts to run.')
            
    def write(self, dest=None, *args, **kwargs):
        log.info('Writing output to destination %s.' % dest)
        self.df.clean(dest=dest)
        self.df.write(dest=dest, *args, **kwargs)
        
    def backup(self, dest=None, skipfails=False):
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
