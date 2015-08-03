import pydwarf
import raws

default_species = [
    'DWARF', 'ELF', 'HUMAN', 'GOBLIN', 'KOBOLD', 'GREMLIN',
    'TROLL', 'OGRE', 'DRAGON', 'GIANT', 'CYCLOPS',
    'ETTIN', 'MINOTAUR', 'YETI', 'SASQUATCH', 'FAIRY',
    'PIXIE', 'MERPERSON'
]

additional_castes = {
    'TRANS_FEMALE': {
        'description': 'She is transsexual, and identifies as female.',
        'addtokens': '[FEMALE][SET_BP_GROUP:BY_TYPE:LOWERBODY][BP_ADD_TYPE:GELDABLE]'
    },
    'TRANS_MALE': {
        'description': 'He is transsexual, and identifies as male.',
        'addtokens': '[MALE]'
    },
    'INTERSEX_FEMALE': {
        'description': 'She is intersex, and identifies as female.',
        'addtokens': '[FEMALE]'
    },
    'INTERSEX_MALE': {
        'description': 'He is intersex, and identifies as male.',
        'addtokens': '[MALE]'
    }
}

add_trans_tokens = '[CAN_DO_INTERACTION:SMEEPROCKET_STERILE][CDI:TARGET:A:SELF_ONLY][CDI:WAIT_PERIOD:100][CDI:FREE_ACTION][POP_RATIO:1]'
add_beard_tokens = '[BODY_DETAIL_PLAN:FACIAL_HAIR_TISSUE_LAYERS]'

add_sterile_interaction = '''
[INTERACTION:SMEEPROCKET_STERILE]
[I_SOURCE:CREATURE_ACTION]
[I_TARGET:A:CREATURE]
[IT_CANNOT_TARGET_IF_ALREADY_AFFECTED][IT_CANNOT_HAVE_SYNDROME_CLASS:CELIBACY]
[IT_LOCATION:CONTEXT_CREATURE]
[I_EFFECT:ADD_SYNDROME]
[IE_TARGET:A]
[IE_IMMEDIATE]
[SYNDROME][SYN_CLASS:CELIBACY]
[CE_ADD_TAG:STERILE:START:0]
'''

@pydwarf.urist(
    name = 'smeeprocket.transgender',
    version = '1.0.1',
    author = ('SmeepRocket', 'Sophie Kirschner'),
    description = 'Adds transgender and intersex castes to creatures.',
    arguments = {
        'species': '''An iterable containing each species that should be given transgender
            and intersex castes.''',
        'beards': '''If True, all dwarf castes will be given beards. If False, none of the
            added castes will have beards for any species. Defaults to True.''',
        'frequency': '''Higher numbers cause rarer incidence of added castes.'''
    },
    compatibility = pydwarf.df_0_40
)
def trans(dfraws, species=default_species, beards=True, frequency=500):
    # Add new interaction
    pydwarf.log.debug('Adding sterility interaction...')
    objinteraction = dfraws.get('OBJECT:INTERACTION')
    if objinteraction:
        objinteraction.add(pretty=add_sterile_interaction)
    else:
        return pydwarf.failure('Unable to add sterility interaction.')
    
    # Add new castes
    castefailures = []
    creaturetokens = dfraws.allobj(type='CREATURE', id_in=species)
    for creaturetoken in creaturetokens:
        pydwarf.log.debug('Handling creature %s...' % creaturetoken)
        
        castes = creaturetoken.allprop(exact_value='CASTE', args_count=1)
        if len(castes) == 2 and ((castes[0].args[0] == 'MALE' and castes[1].args[0] == 'FEMALE') or (castes[1].args[0] == 'MALE' and castes[0].args[0] == 'FEMALE')):
            
            # Remove DESCRIPTION token from the creature and add it to each caste
            descriptiontoken = creaturetoken.get(exact_value='DESCRIPTION', args_count=1)
            if descriptiontoken:
                descriptiontoken.remove()
                for castetoken in castes: castetoken.add(token=descriptiontoken.copy())
            
            # Handle existing castes
            for caste in castes:
                # Add beards to dwarven women
                if beards and caste.args[0] == 'FEMALE': caste.add(pretty=add_beard_tokens)
                # Add population ratio token
                caste.add(raws.token(value='POP_RATIO', args=[str(frequency)]))
            
            # Add each new caste
            for castename, castedict in additional_castes.iteritems():
                castetoken = castes[0].add(raws.token(value='CASTE', args=[castename]), reverse=True)
                # Every new caste gets these tokens
                castetoken.add(pretty=add_trans_tokens)
                # Add beards to new dwarf castes
                if beards and creaturetoken.arg() == 'DWARF': castetoken.add(pretty=add_beard_tokens)
                # Tokens unique to each new caste
                if 'addtokens' in castedict: castetoken.add(pretty=castedict['addtokens'])
                # Add the caste-specific description
                description = ' '.join((descriptiontoken.args[0], castedict['description'])) if descriptiontoken else castedict['description']
                castetoken.add(raws.token(value='DESCRIPTION', args=[description]))
                
        else:
            pydwarf.log.error('Unexpected castes for creature %s: %s.' % (
                creaturetoken,
                ', '.join(str(caste) for caste in castes)
            ))
            castefailures.append(creaturetoken)

    if len(castefailures) == 0:
        return pydwarf.success('Added new castes to %d creatures.' % len(species))
    else:
        return pydwarf.failure('Added new castes to %d creatures, but failed to add castes to %s.' % (len(species) - len(castefailures), castefailures))
    