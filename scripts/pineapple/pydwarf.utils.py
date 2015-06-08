import pydwarf
import raws



@pydwarf.urist(
    name = 'pineapple.utils.addtoentity',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''A simple utility script which adds tokens to entities.''',
    arguments = {
        'entities': 'Adds tokens to these entities.',
        '**kwargs': ''''Should map keywords to iterables. For example, setting the argument
            permitted_job=('MINER', 'CARPENTER') would result in the tokens
            [PERMITTED_JOB:MINER] and [PERMITTED_JOB:CARPENTER] being added to each of the
            listed entities if they aren't present already.'''
    },
    compatibility = '.*'
)
def addtoentity(df, entities, **kwargs):
    pydwarf.log.debug('Adding tokens to %d entities.' % len(entities))
    added = 0
    entitytokens = df.allobj(type='ENTITY', id_in=entities)
    if len(entitytokens) != len(entities):
        return pydwarf.failure()
    else:
        for permittype, permititems in kwargs.iteritems():
            permitvalue = permittype.upper()
            pydwarf.log.debug('Handling tokens of type %s.' % permitvalue)
            for permititem in permititems:
                for entitytoken in entitytokens:
                    if not entitytoken.getprop(exact_value=permitvalue, exact_args=(permititem,)):
                        entitytoken.addprop(raws.token(value=permitvalue, args=[permititem]))
                        added += 1
        return pydwarf.success('Added %d permitted things to %d entities.' % (added, len(entitytokens)))



@pydwarf.urist(
    name = 'pineapple.utils.addreaction',
    version = '1.0.0',
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
    if permit_entities is not None and (not addtoentity(df, permit_entities, permitted_reaction=(id,)).success):
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
