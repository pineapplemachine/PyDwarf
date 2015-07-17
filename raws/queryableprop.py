#!/usr/bin/env python
# coding: utf-8

import queryable



class queryableprop(queryable.queryable):
    
    # Inheriting classes must implement a propterminationfilter method
    
    def getprop(self, *args, **kwargs):
        return self.propquery(self.get, *args, **kwargs)
    
    def lastprop(self, *args, **kwargs):
        return self.propquery(self.last, *args, **kwargs)
    
    def allprop(self, *args, **kwargs):
        return self.propquery(self.all, *args, **kwargs)
        
    def propquery(self, method, *args, **kwargs):
        return method(*args, filters=self.propterminationfilter(), **kwargs)
