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
        '''Get the first object token matching a given type and id. (If there's more 
            than one result for any given query then I'm afraid you've done something
            silly with your raws.) This method should work properly with things like
            CREATURE:X tokens showing up in entity_default. Should almost always be
            faster than an equivalent call to get, also.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> print dwarf.list(include_self=True, range=4)
                [CREATURE:DWARF]
                [DESCRIPTION:A short, sturdy creature fond of drink and industry.]
                [NAME:dwarf:dwarves:dwarven]
                [CASTE_NAME:dwarf:dwarves:dwarven]
            >>> not_dwarf = df.getlast('CREATURE:DWARF') # gets the CREATURE:DWARF token underneath ENTITY:MOUNTAIN instead
            >>> print not_dwarf.list(include_self=True, range=4)
                [CREATURE:DWARF]
                [TRANSLATION:DWARF]
                [DIGGER:ITEM_WEAPON_PICK]
                [WEAPON:ITEM_WEAPON_AXE_BATTLE]
        '''
            
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
        '''Gets all objects matching a given type and optional id or id regex.
        
        Example usage:
            >>> pants = df.allobj('ITEM_PANTS')
            >>> print pants
            [ITEM_PANTS:ITEM_PANTS_PANTS]
            [ITEM_PANTS:ITEM_PANTS_GREAVES]
            [ITEM_PANTS:ITEM_PANTS_LEGGINGS]
            [ITEM_PANTS:ITEM_PANTS_LOINCLOTH]
            [ITEM_PANTS:ITEM_PANTS_THONG]
            [ITEM_PANTS:ITEM_PANTS_SKIRT]
            [ITEM_PANTS:ITEM_PANTS_SKIRT_SHORT]
            [ITEM_PANTS:ITEM_PANTS_SKIRT_LONG]
            [ITEM_PANTS:ITEM_PANTS_BRAIES]
            >>> bears = df.allobj(type='CREATURE', re_id='BEAR_.+')
            >>> print bears
            [CREATURE:BEAR_GRIZZLY]
            [CREATURE:BEAR_BLACK]
            [CREATURE:BEAR_POLAR]
            [CREATURE:BEAR_SLOTH]
        '''
        
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
        '''Calls allobj with the same arguments then adds each result to a dictionary
        associating object IDs with the tokens where they're declared.
        
        Example usage:
            >>> inorganics = df.objdict('INORGANIC')
            >>> print len(inorganics)
            263
            >>> print 'NOT_A_ROCK' in inorganics
            False
            >>> obsidian = inorganics.get('OBSIDIAN')
            >>> print obsidian.list(range=6, include_self=True)
            [INORGANIC:OBSIDIAN]
            [USE_MATERIAL_TEMPLATE:STONE_TEMPLATE]
                [MELTING_POINT:13600]
                [BOILING_POINT:16000]
                [IMPACT_YIELD:1000000]
                [IMPACT_FRACTURE:1000000]
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
