import pydwarf
import raws



@pydwarf.urist(
    name = 'pineapple.utils.addtoentity',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''A simple utility script which adds tokens to entities.''',
    arguments = {
        'entities': 'Adds tokens to these entities.',
        'tokens': 'A string or collection of tokens to add to each entity.',
        'check_existing': '''If set to True then before adding the tokens an entity will first
            be checked for whether it already has any of the given tokens. If it does then none
            of the given tokens will be added to that entity.'''
    },
    compatibility = '.*'
)
def addtoentity(df, entities, tokens, check_existing=True):
    if isinstance(entities, basestring): entities = (entities,)
    if isinstance(tokens, basestring): tokens = raws.token.parse(tokens)
    pydwarf.log.debug('Adding tokens to %d entities.' % len(entities))
    entitytokens = df.allobj(type='ENTITY', id_in=entities)
    
    for entitytoken in entitytokens:
        if check_existing and any(entitytoken.getprop(match_token=token) for token in tokens):
            pydwarf.log.debug('Skipping entity %s because it already contains a token that would have been added.' % entitytoken)
        else:
            entitytoken.addprop(tokens)
        
    if len(entitytokens) != len(entities):
        return pydwarf.failure('Failed to add tokens to all given entities because only %d of %d exist.' % (len(entitytokens), len(entities)))
    else:
        return pydwarf.success('Added tokens to %d entities.' % len(entitytokens))



@pydwarf.urist(
    name = 'pineapple.utils.addreaction',
    version = '1.0.1',
    author = 'Sophie Kirschner',
    description = '''A simple utility script which adds a single reaction.''',
    arguments = {
        'id': 'ID of the reaction to add.',
        'tokens': 'The tokens that should be added immediately after the REACTION:ID token.',
        'add_to_file': 'Adds the reaction to this file. Defaults to reaction_custom.',
        'permit_entities': '''An iterable containing entities to which to add
            PERMITTED_REACTION tokens to. When set to None, no such tokens will be added.'''
    },
    compatibility = '.*'
)
def addreaction(df, id, tokens, add_to_file='reaction_custom', permit_entities=None):
    if permit_entities is not None and (not addtoentity(df, permit_entities, 'PERMITTED_REACTION:%s' % id).success):
        return pydwarf.failure('Failed to add permitted reactions to entites.')
    else:
        if df.getobj(type='REACTION', exact_id=id):
            return pydwarf.failure('Reaction %s already exists.' % id)
        else:
            rfile = df.getfile(add_to_file, create='OBJECT:REACTION')
            rfile.add(raws.token(value='REACTION', args=[id], prefix='\n\n')).add(tokens)
            return pydwarf.success('Added reaction %s to file %s and entities %s.' % (id, add_to_file, permit_entities))
    


@pydwarf.urist(
    name = 'pineapple.utils.objecttokens',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Utility script for adding or removing tokens from
        objects.''',
    arguments = {
        'object_type': '''The type of object which should be affected.''',
        'token': '''The token to be added or removed.''',
        'remove_from': '''If set to None, no matching tokens are removed. If
            set to '*', all matching tokens are removed. If set to an
            iterable containing IDs of objects, matching tokens will be
            removed from each of those objects.''',
        'add_to': '''If set to None, no tokens tokens are added. If set to
            '*', tokens are added to all objects. If set to an iterable
            containing IDs of objects, tokens will be added to each of
            those objects.'''
    },
    compatibility = '.*'
)
def objecttokens(df, object_type, token, add_to=None, remove_from=None):
    added, removed = 0, 0
    
    # Remove tokens
    if remove_from:
        for objtoken in df.allobj(type=object_type, id_in=(None if remove_from == '*' else remove_from)):
            for removetoken in objtoken.allprop(token): 
                removetoken.remove()
                removed += 1
        
    # Add tokens
    if add_to:
        for objtoken in df.allobj(type=object_type, id_in=(None if add_to == '*' else add_to)):
            if not objtoken.getprop(token):
                objtoken.addprop(token)
                added += 1
        
    # All done!
    if removed or added:
        return pydwarf.success('Added %d %s tokens and removed %d from object type %s.' % (added, token, removed, object_type))
    else:
        return pydwarf.failure('Didn\'t add or remove any %s tokens.' % token)  



@pydwarf.urist(
    name = 'pineapple.utils.addhack',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Utility script for adding a new DFHack script.''',
    arguments = {
        'name': 'The file name of the script to add.',
        'auto_run': '''If set to True, a line will be added to dfhack.init containing only
            the name of the added script. If set to None, no such line will be added. If set
            to an arbitrary string, that string will be added as a new line at the end of
            dfhack.init.''',
        '**kwargs': '''Other named arguments will be passed on to the dir.add method used to
            create the file object corresponding to the added script.'''
    },
    compatibility = '.*'
)
def addhack(df, name, auto_run, **kwargs):
    pydwarf.log.debug('Adding new file %s.' % name)
    file = df.add(name=name, **kwargs)
    
    if auto_run:
        if auto_run is True: auto_run = '\n%s' % file.name
        pydwarf.log.debug('Appending line %s to the end of dfhack.init.' % auto_run)
        
        if 'dfhack.init' not in df:
            if 'dfhack.init-example' in df:
                pydwarf.log.info('Copying dfhack.init-example to new file dfhack.init before adding new content to the file.')
                init = df['dfhack.init-example'].copy().bin()
                init.name = 'dfhack.init'
                df.add(file=init)
            else:
                return pydwarf.failure('Failed to locate dfhack.init or dfhack.init-example.')
        else:
            init = df['dfhack.init'].bin()
        
        init.add('\n%s # Added by PyDwarf\n' % auto_run)
        return pydwarf.success('Added new file %s and appended line %s to dfhack.init.' % (name, auto_run))
        
    else:
        return pydwarf.success('Added new file %s.' % name)



@pydwarf.urist(
    name = 'pineapple.utils.addobject',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Utility script for adding a new object to the raws.''',
    arguments = {
        'add_to_file': '''The name of the file to add the object to. If it doesn't exist already
            then the file is created anew. The string is formatted such that %(type)s is
            replaced with the object_header, lower case.''',
        'tokens': '''The tokens belonging to the object to create.''',
        'type': '''Specifies the object type. If type and id are left unspecified, the first
            token of the tokens argument is assumed to be the object's [TYPE:ID] token and the
            type and id arguments are taken out of that.''',
        'id': '''Specifies the object id. If type and id are left unspecified, the first
            token of the tokens argument is assumed to be the object's [TYPE:ID] token and the
            type and id arguments are taken out of that.''',
        'permit_entities': '''For relevant object types such as reactions, buildings, and items,
            if permit_entities is specified then tokens are added to those entities to permit
            the added object.''',
        'item_rarity': '''Most items, when adding tokens to entities to permit them, accept an
            optional second argument specifying rarity. It should be one of 'RARE', 'UNCOMMON',
            'COMMON', or 'FORCED'. This argument can be used to set that rarity.''',
        'object_header': '''When the object is added to a file which doesn't already exist,
            an [OBJECT:TYPE] token must be added at its beginning. This argument, if specified,
            provides the type in that token. Otherwise, when the argument is left set to None,
            the type will be automatically decided.'''
    },
    compatibility = '.*'
)
def addobject(df, add_to_file, tokens, type=None, id=None, permit_entities=None, item_rarity=None, object_header=None):
    # If type and id weren't explicitly given then assume the first given token is the TYPE:ID header and get the info from there.
    header_in_tokens = type is None and id is None
    header = None
    if header_in_tokens:
        if isinstance(tokens, basestring): tokens = raws.token.parse(tokens)
        header = tokens[0]
        type = header.value
        id = header.arg()
        pydwarf.log.debug('Extracted object type %s and id %s from given tokens.' % (type, id))
        
    # Get the applicable object dict which knows how to map TYPE:ID to its corresponding OBJECT:TYPE header.
    if object_header is None:
        object_header = raws.objects.headerforobject(type)
    
    # If add_to_file already exists, fetch it. Otherwise add it to the raws.
    add_to_file = add_to_file % {'type': object_header.lower()}
    if add_to_file in df:
        file = df.getfile(file)
    else:
        file = df.add(add_to_file)
        file.add(raws.token(value='OBJECT', args=[object_header]))
        pydwarf.log.debug('Added new file %s to dir.' % add_to_file)
    
    # Add the object itself to the raws.
    if not header_in_tokens: header = file.add(raws.token(value=type, args=[id]))
    file.add(tokens)
    
    # Add tokens to entities to permit the use of this object.
    if permit_entities:
        response = permitobject(
            df,
            type = type,
            id = id,
            permit_entities = permit_entities,
            item_rarity = item_rarity
        )
        if not response: return response
            
    # All done!
    return pydwarf.success('Added object %s to file %s.' % (header, file))



@pydwarf.urist(
    name = 'pineapple.utils.addobjects',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Utility script for adding several new objects to the raws at once.''',
    arguments = {
        'add_to_file': '''The name of the file to add the object to. If it doesn't exist already
            then the file is created anew. The string is formatted such that %(type)s is
            replaced with the object_header, lower case.''',
        'objects': '''An iterable containing tokens belonging to the objects to add.''',
        '**kwargs': 'Passed on to pineapple.utils.addobject.',
    },
    compatibility = '.*'
)
def addobjects(df, add_to_file, objects, **kwargs):
    for obj in objects:
        response = addobject(df, add_to_file, **kwargs)
        if not response.success: return response
    return response.success('Added %d objects.' % len(objects))



@pydwarf.urist(
    name = 'pineapple.utils.permitobject',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Utility script for permitting an object with entities.''',
    arguments = {
        'type': '''Specifies the object type.''',
        'id': '''Specifies the object id.''',
        'permit_entities': '''For relevant object types such as reactions, buildings, and items,
            if permit_entities is specified then tokens are added to those entities to permit
            the added object.''',
        'item_rarity': '''Some items, when adding tokens to entities to permit them, accept an
            optional second argument specifying rarity. It should be one of 'RARE', 'UNCOMMON',
            'COMMON', or 'FORCED'. This argument can be used to set that rarity.'''
    },
    compatibility = '.*'
)
def permitobject(df, type=None, id=None, permit_entities=None, item_rarity=None):
    # Decide what tokens need to be added to the entities based on the object type
    if type == 'REACTION':
        tokens = raws.token(exact_value='PERMITTED_REACTION', args=[id])
    elif type.startswith('BUILDING_'):
        tokens = raws.token(exact_value='PERMITTED_BUILDING', args=[id])
    elif type.startswith('ITEM_'):
        value = type.split('_')[1]
        args = [id, item_rarity] if item_rarity else [id]
        tokens = raws.token(value=value, args=args)
    else:
        tokens = None
    
    # Actually add those tokens
    if tokens is None:
        return pydwarf.success('Didn\'t actually permit object [%s:%s] because objects of this type cannot be permitted.' % (type, id))
    elif not permit_entities:
        return pydwarf.failure('No entities were given for permitting.')
    else:
        response = addtoentity(
            df,
            entities = permit_entities, 
            tokens = tokens
        )
        if not response:
            return response
        else:
            return pydwarf.success('Permitted object [%s:%s] for %d entities.' % (type, id, len(permit_entities)))
    
    
    
@pydwarf.urist(
    name = 'pineapple.utils.permitobjects',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Utility script for permitting several objects at once with entities.''',
    arguments = {
        'objects': '''An iterable containing type, id tuples for objects to permit.''',
        '**kwargs': 'Passed on to pineapple.utils.permitobject.',
    },
    compatibility = '.*'
)
def permitobjects(df, objects, **kwargs):
    for item in objects:
        if isinstance(item, raws.token):
            type, id = item.value, item.arg()
        elif isinstance(item, basestring):
            type, id = item.split(':')
        else:
            type, id = item
        response = permitobject(df, type, id, **kwargs)
        if not response: return response
    return pydwarf.success('Permitted %d objects.' % len(objects))
    