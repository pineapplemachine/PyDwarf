#!/usr/bin/env python
# coding: utf-8

import queryable



class queryableadd(queryable.queryable):
    
    # Inheriting classes must implement an add method
    
    def setsingular(self, getmethod, addmethod, *args, **kwargs):
        setvalue, setargs = queryableadd.argsset(*args, **kwargs)
        applytoken = getmethod(exact_value=setvalue)
        if applytoken is None:
            return addmethod(value=setvalue, args=setargs)
        else:
            applytoken.args.reset(setargs)
            return applytoken
            
    def setplural(self, getmethod, *args, **kwargs):
        setvalue, setargs = queryableadd.argsset(*args, **kwargs)
        settoken = token.token.autosingular(*args, **kwargs)
        applytokens = getmethod(exact_value=setvalue)
        for applytoken in applytokens: applytoken.args.reset(setargs)
        return applytokens
        
    @staticmethod
    def argsset(*args, **kwargs):
        if len(args) == 2:
            setvalue = args[0]
            setargs = args[1]
            if isinstance(setargs, basestring) or not (hasattr(setargs, '__iter__') or hasattr(setargs, '__getitem__')):
                setargs = (setargs,)
        else:
            settoken = token.token.autosingular(*args, **kwargs)
            setvalue = settoken.value
            setargs = settoken.args
        return setvalue, setargs
            
    def set(self, *args, **kwargs):
        return self.setsingular(self.get, self.add, *args, **kwargs)
        
    def setlast(self, *args, **kwargs):
        return self.setsingular(self.last, self.add, *args, **kwargs)
            
    def setall(self, *args, **kwargs):
        return self.setplural(self.all, *args, **kwargs)



import token
