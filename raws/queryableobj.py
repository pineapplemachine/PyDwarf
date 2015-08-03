#!/usr/bin/env python
# coding: utf-8

import queryable



class queryableobj(queryable.queryable):
    
    # Inheriting classes must implement a getobjheaders method
    
    def getobjheadername(self, type):
        version = self if hasattr(self, 'config') or hasattr(self, 'version') else self.dir
        if type is None:
            return objects.headers(version)
        else:
            return (objects.headerforobject(type, version),)
    
    def headersfortype(self, type=None, type_in=None):
        if type or (type_in is None):
            headers = self.getobjheaders(type)
        else:
            headers = []
        if type_in:
            for itertype in type_in: 
                for header in self.getobjheaders(itertype):
                    if not any(header is h for h in headers): headers.append(header)
        return headers
        
    def removeobj(self, *args, **kwargs):
        obj = self.getobj(*args, **kwargs)
        if obj: obj.removeselfandprops()
        return obj
    def removeallobj(self, *args, **kwargs):
        objects = self.allobj(*args, **kwargs)
        for obj in objects: obj.removeselfandprops()
        return objects
        
    def getobj(self, pretty=None, type=None, exact_id=None, type_in=None, re_id=None, id_in=None):
        '''Get the first object token matching a given type and id.'''
            
        type, exact_id = queryableobj.objpretty(pretty, type, exact_id)
        headers = self.headersfortype(type, type_in)
        if type is None and type_in is None: type_in = objects.objects()
        for objecttoken in headers:
            obj = objecttoken.get(
                exact_value = type,
                value_in = type_in,
                exact_args = (exact_id,) if exact_id else None,
                re_args = (re_id,) if re_id else None,
                arg_in = ((0, id_in),) if id_in else None,
                args_count = 1
            )
            if obj: return obj
        return None
        
    def lastobj(self, pretty=None, type=None, exact_id=None, type_in=None, re_id=None, id_in=None): 
        '''Get the last object token matching a given type and id.'''
        
        type, exact_id = queryableobj.objpretty(pretty, type, exact_id)
        headers = self.headersfortype(type, type_in)
        if type is None and type_in is None: type_in = objects.objects()
        for objecttoken in headers:
            obj = objecttoken.last(
                exact_value = type,
                value_in = type_in,
                exact_args = (exact_id,) if exact_id else None,
                re_args = (re_id,) if re_id else None,
                arg_in = ((0, id_in),) if id_in else None,
                args_count = 1
            )
            if obj: return obj
        return None
        
    def allobj(self, pretty=None, type=None, exact_id=None, type_in=None, re_id=None, id_in=None):
        '''Get all object tokens matching a given type and id.'''
        
        type, exact_id = queryableobj.objpretty(pretty, type, exact_id)
        results = tokenlist.tokenlist()
        headers = self.headersfortype(type, type_in)
        if type is None and type_in is None: type_in = objects.objects()
        for objecttoken in headers:
            for result in objecttoken.all(
                exact_value = type,
                value_in = type_in,
                exact_args = (exact_id,) if exact_id else None,
                re_args = (re_id,) if re_id else None,
                arg_in = ((0, id_in),) if id_in else None,
                args_count = 1
            ):
                results.append(result)
        return results
        
    def objdict(self, *args, **kwargs):
        '''
            Calls allobj with the same arguments then adds each result to a
            dictionary associating object IDs with the tokens where they're
            declared.
        '''
        return {token.args[0]: token for token in self.allobj(*args, **kwargs)}
        
    @staticmethod
    def objpretty(pretty, type, id):
        '''Internal: Used for handling getobj/allobj arguments.'''
        if pretty is not None:
            if ':' in pretty:
                parts = pretty.split(':')
                if len(parts) != 2: raise ValueError('Failed to parse argument because there were too many or too few colons, there ought to be be just one.')
                return parts[0], parts[1]
            elif type is None:
                return pretty, id
            elif id is None:
                return pretty, type
        else:
            return type, id



import objects
import tokenlist
