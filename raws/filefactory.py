#!/usr/bin/env python
# coding: utf-8

import os

import reffile
import binfile
import rawfile



binnames = [
    'dfhack.init',
    'dfhack.init-example',
]

rawnames = [
    'init.txt',
    'd_init.txt',
    'colors.txt',
    'interface.txt',
    'announcements.txt',
    'world_gen.txt',
    'overrides.txt',
]



def filefactory(path, log=None, **kwargs): # TODO: move this elsewhere and make it more easily configurable
    basename = os.path.basename(path)
    try:
        if basename.endswith('.txt'):
            with open(path, 'rb') as txt:
                if txt.readline().strip() == os.path.splitext(basename)[0]:
                    txt.seek(0)
                    return rawfile.rawfile(path=path, file=txt, **kwargs)
        elif basename in binnames:
            return binfile.binfile(path=path, **kwargs)
        elif basename in rawnames:
            return rawfile.rawfile(path=path, file=txt, **kwargs)
    
    except Exception as e:
        if log:
            log.warning('Failed to read file from path %s. Defauling to reading as a reffile, which should (hopefully) work despite.' % path)
            log.debug(traceback.format_exc())
    
    return reffile.reffile(path=path, **kwargs)
