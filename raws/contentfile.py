#!/usr/bin/env python
# coding: utf-8

import basefile



class contentfile(basefile.basefile):
    def __init__(self):
        self.content = None
        
    def getcontent(self):
        return self.content
        
    def setcontent(self, content):
        self.content = content
