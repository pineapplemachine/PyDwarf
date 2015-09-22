#!/usr/bin/env python
# coding: utf-8

import queryable



class queryableprop(queryable.queryable):
    
    # Inheriting classes must implement a propterminationfilter method
    
    def getprop(self, *args, **kwargs):
        '''Get the first matching property belonging to an object.'''
        return self.propquery(self.get, *args, **kwargs)
    
    def lastprop(self, *args, **kwargs):
        '''Get the last matching property belonging to an object.'''
        return self.propquery(self.last, *args, **kwargs)
    
    def allprop(self, *args, **kwargs):
        '''Get all matching properties belonging to an object.'''
        return self.propquery(self.all, *args, **kwargs)
        
    def propquery(self, method, *args, **kwargs):
        '''Internal: Generalized prop query.'''
        return method(*args, prefilters=self.propterminationfilter(), **kwargs)
        
    def removeprop(self, *args, **kwargs):
        '''Remove the first property matching some filter.'''
        token = self.getprop(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removelastprop(self, *args, **kwargs):
        '''Remove the last property matching some filter.'''
        token = self.getlastprop(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removeallprop(self, *args, **kwargs):
        '''Remove all properties matching some filter.'''
        tokens = self.allprop(*args, **kwargs)
        for token in tokens: token.remove()
        return tokens
