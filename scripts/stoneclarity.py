# vim:fileencoding=UTF-8

import pydwarf
from raws import rawstokenquery

# Generic mutators for use in rules
def mutator_generic(value, *args):
    def fn(inorganic):
        tokenresult = inorganic.stoneclarity[value]
        if tokenresult and len(tokenresult):
            token = tokenresult[0]
            for i in xrange(min(len(args), len(token.args))):
                if args[i] is not None: token.args[i] = args[i]
    return fn
def mutator_remove(value):
    def fn(inorganic):
        tokenresult = inorganic.stoneclarity[value]
        if tokenresult:
            for result in tokenresult: result.remove()
    return fn

# Default to these rules when none are passed
default_rules = [
    # Make all flux stone have a white foreground
    {
        # Gives the rule a name, makes logs pretty
        'name': 'flux',
        # Indicates that this rule applies to inorganics in the FLUX group: That is, ones which have a
        # [REACTION_CLASS:FLUX] token in their properties.
        'group': 'FLUX',
        # Each given mutator function is run for each matching inorganic, with that token as the argument.
        # Tokens will have a stoneclarity attribute which contains the results of the query which targeted it.
        # Here, mutator_generic returns a closure in order to keep things convenient.
        'mutator': mutator_generic('DISPLAY_COLOR', 7, None, 1)
    },
    # Make all fuel be represented by * on the map and in stockpiles
    {
        'name': 'fuel',
        'group': 'FUEL',
        'mutator': (mutator_generic('TILE', "'*'"), mutator_generic('ITEM_SYMBOL', "'*'"))
    },
    # Make cobaltite not look like ore
    {
        'name': 'cobaltite',
        'id': 'COBALTITE',
        'mutator': (mutator_generic('TILE', "'%'"), mutator_remove('ITEM_SYMBOL'))
    },
    # Make all ores be represented by £ on the map and * in stockpiles
    {
        'name': 'ore',
        'group': 'ORE',
        'mutator': (mutator_generic('TILE', '156'), mutator_generic('ITEM_SYMBOL', "'*'"))
    },
    # Make all gems be represented by ☼ on the map and in stockpiles
    {
        'name': 'gem',
        'group': 'GEM',
        'mutator': (mutator_generic('TILE', '15'), mutator_generic('ITEM_SYMBOL', '15'))
    }
]

# You should specify fuels=vanilla_fuels if you know that no prior mod has modified DF's fuels
vanilla_fuels = ['COAL_BITUMINOUS', 'LIGNITE']

# Pass this dict when querying, starting with some INORGANIC, to find relevant tokens all in one go
# ENVIRONMENT, ENVIRONMENT_SPEC, and FUEL groups are handled specially. Everything else is simply
# a boolean check for a match, and matches get placed in the group identified by the key to which
# a token query is matched.
def propertyquery(**kwargs): return rawstokenquery(limit=1, limit_terminates=False, **kwargs) # Convenience function
default_inorganics_query = {
    # Detect tokens which indicate what kind of inorganic this is
    'STONE': propertyquery(exact_value='IS_STONE'),
    'GEM': propertyquery(exact_value='IS_GEM'),
    'ORE': propertyquery(exact_value='METAL_ORE'),
    'FLUX': propertyquery(pretty='REACTION_CLASS:FLUX'),
    'GYPSUM': propertyquery(pretty='REACTION_CLASS:GYPSUM'),
    'SOIL': propertyquery(exact_value='SOIL'),
    'SOIL_SAND': propertyquery(exact_value='SOIL_SAND'),
    'SOIL_OCEAN': propertyquery(exact_value='SOIL_OCEAN'),
    'METAMORPHIC': propertyquery(exact_value='METAMORPHIC'),
    'SEDIMENTARY': propertyquery(exact_value='SEDIMENTARY'),
    'IGNEOUS_ALL': propertyquery(exact_value='IGNEOUS_ALL'),
    'IGNEOUS_EXTRUSIVE': propertyquery(exact_value='IGNEOUS_EXTRUSIVE'),
    'IGNEOUS_INTRUSIVE': propertyquery(exact_value='IGNEOUS_INTRUSIVE'),
    'AQUIFER': propertyquery(exact_value='AQUIFER'),
    'NO_STONE_STOCKPILE': propertyquery(exact_value='NO_STONE_STOCKPILE'),
    'ENVIRONMENT': rawstokenquery(exact_value='ENVIRONMENT'),
    'ENVIRONMENT_SPEC': rawstokenquery(exact_value='ENVIRONMENT_SPEC'),
    # Detect tokens which represent appearance
    'TILE': propertyquery(exact_value='TILE'),
    'ITEM_SYMBOL': propertyquery(exact_value='ITEM_SYMBOL'),
    'DISPLAY_COLOR': propertyquery(exact_value='DISPLAY_COLOR'),
    'BASIC_COLOR': propertyquery(exact_value='BASIC_COLOR'),
    'TILE_COLOR': propertyquery(exact_value='TILE_COLOR'),
    'STATE_COLOR': propertyquery(exact_value='STATE_COLOR'),
    # Stop at the next [INORGANIC:] token
    'EOF': rawstokenquery(exact_value='INORGANIC', limit=1)
}

# Automatically get a list of INORGANIC IDs which describe fuels
def autofuels(raws, log=True):
    if log: pydwarf.log.info('No fuels specified, detecting...')
    fuels = []
    for reaction in raws.all(exact_value='REACTION'): # For each reaction:
        # Does this reaction produce coke?
        reactionmakescoke = False
        for product in reaction.alluntil(exact_value='PRODUCT', until_exact_value='REACTION'):
            if product.args[-1] == 'COKE':
                if log: pydwarf.log.debug('Found coke-producing reaction %s with product %s.' % (reaction, product))
                reactionmakescoke = True
                break
        if reactionmakescoke:
            for reagent in reaction.alluntil(exact_value='REAGENT', until_exact_value='REACTION'):
                if log: pydwarf.log.debug('Identified reagent %s as referring to a fuel.' % (reagent))
                fuels.append(reagent.args[-1])
    if log: pydwarf.log.info('Finished detecting fuels! These are the ones I found: %s' % fuels)
    if not len(fuels): pydwarf.log.warning('Oops, failed to find any fuels.')
    return fuels

# Build dictionaries which inform stoneclarity of how various inorganics might be identified
def builddicts(raws, fuels, log=True):
    if log: pydwarf.log.info('Building dicts...')
    groups = {}
    ids = {}
    inorganics = raws.all(exact_value='INORGANIC')
    if log: pydwarf.log.info('I found %d inorganics. Processing...' % len(inorganics))
    for token in inorganics:
        # Get results of query
        query = token.query(inorganics_query)
        token.stoneclarity = {i: j.result for i, j in query.iteritems()}
        # Handle the simpler groups, 1:1 correspondence between whether some property was found and whether the inorganic belongs in some group
        for groupname in token.stoneclarity:
            if groupname not in ('FUEL', 'ENVIRONMENT', 'ENVIRONMENT_SPEC') and len(token.stoneclarity[groupname]):
                if groupname not in groups: groups[groupname] = []
                groups[groupname].append(token)
        # Handle metamorphic, sedimentary, igneous
        # Also veins and clusters, etc.
        for env in token.stoneclarity['ENVIRONMENT']:
            if env.nargs >= 2:
                envtype = 'ENVIRONMENT_'+env.args[0]
                veintype = env.args[1]
                if envtype not in groups: groups[envtype] = []
                if veintype not in groups: groups[veintype] = []
                groups[envtype].append(token)
                groups[veintype].append(token)
        for env in token.stoneclarity['ENVIRONMENT_SPEC']:
            if env.nargs >= 2:
                spectype = 'ENVIRONMENT_SPEC_'+env.args[0]
                veintype = env.args[1]
                if spectype not in groups: groups[spectype] = []
                if veintype not in groups: groups[veintype] = []
                groups[envtype].append(token)
                groups[veintype].append(token)
        # Handle ids and fuels
        if token.nargs == 1:
            id = token.args[0]
            ids[id] = token
            if id in fuels:
                if 'FUEL' not in groups: groups['FUEL'] = []
                groups['FUEL'].append(token)
    if log: pydwarf.log.info('Finished building dicts! Found %d groups and %d ids.' % (len(groups), len(ids)))
    return groups, ids

# From dicts built by builddicts and given a rule, return a list of inorganics which match that rule
def getrulematches(rule, groups, ids):
    matches = []
    if 'group' in rule:
        matchgroups = (rule['group'],) if isinstance(rule['group'], basestring) else rule['group']
        for groupname in matchgroups:
            if groupname in groups: matches += groups[groupname]
    if 'id' in rule:
        matchids = (rule['id'],) if isinstance(rule['id'], basestring) else rule['id']
        for id in matchids:
            if id in ids: matches.append(ids[id])
    return matches
    
# Applies a list of rules to matches based on built dicts
def applyrules(rules, groups, ids, log=True):
    for rule in rules:
        if 'mutator' in rule:
            mutator = rule['mutator']
            matches = getrulematches(rule, groups, ids)
            if log: pydwarf.log.info('Applying %s rule to %d matches...' % (rule['name'] if 'name' in rule else 'unnamed', len(matches)))
            for match in matches:
                if callable(mutator):
                    mutator(match)
                else:
                    for mut in mutator: mut(match)
        else:
            if log: pydwarf.log.warning('Encountered %s rule with no mutators.' % rule['name'] if 'name' in rule else 'unnamed')

@pydwarf.urist(
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Allows powerful editing of the appearances of stone, ore, and gems.',
    arguments = {
        'rules': '''By default makes all flux stone white, makes all fuel use *, makes all ore use £ unmined and * in
            stockpiles, makes cobaltite use % unmined and • in stockpiles, makes all gems use ☼. Specify an object
            other than default_rules to customize behavior, and refer to default_rules as an example of how rules are
            expected to be represented''',
        'query': '''This query is run for each inorganic found and looks for tokens that should be recognized as
            indicators that some inorganic belongs to some group.'''
        'fuels': '''If left unspecified, stoneclarity will attempt to automatically detect which inorganics are fuels.
            If you know that no prior script added new inorganics which can be made into coke then you can cut down a
            on execution time by setting fuels to fuels_vanilla.'''
    }
)
def stoneclarity(raws, rules=default_rules, query=default_inorganics_query, fuels=None):
    if rules and len(rules):
        groups, ids = builddicts(raws, fuels if fuels else autofuels(raws))
        applyrules(rules, groups, ids)
        return pydwarf.success('Finished applying %d rules to %d inorganic groups and %d inorganic ids.' % (len(rules), len(groups), len(ids)))
    else:
        return pydwarf.failure('I was given no rules to follow.')









