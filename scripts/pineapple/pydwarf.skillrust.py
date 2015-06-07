import pydwarf



default_creatures = ['DWARF', 'HUMAN', 'ELF']

default_rates = ('NONE', 'NONE', 'NONE')



@pydwarf.urist(
    name = 'pineapple.skillrust',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Modifies skill rust for given creatures. Disables it entirely by
        default.''',
    arguments = {
        'creatures': 'An iterable containing creatures for which to disable skill rust.',
        'rates': '''What the skill rust rates are to be changed to. It must be a tuple
            or list containing three values. The default is ('NONE', 'NONE', 'NONE'),
            which disables skill rust entirely. Dwarf Fortress's default rates are
            ('8', '16', '16'). Lower numbers indicate faster skill rust.'''
    },
    
    # Though the skill tokens were introduced earlier, a bug persisting until 0.31.18 prevented rust from actually being disabled.
    # http://www.bay12games.com/dwarves/mantisbt/print_bug_page.php?bug_id=2877
    compatibility = (pydwarf.df_revision_range('0.31.18', '0.31.25'), pydwarf.df_0_34, pydwarf.df_0_40)
)
def skillrust(df, creatures=default_creatures, rates=default_rates):
    failures = []
    
    # Handle each creature
    creaturetokens = df.allobj(type='CREATURE', id_in=creatures)
    for creaturetoken in creaturetokens:
        pydwarf.log.debug('Handling skill rust for %s.' % creaturetoken)

        # First see about editing existing skill tokens
        needsnew = True
        editedtotal = 0
        existingtokens = creaturetoken.allprop(value_in=('SKILL_RATE', 'SKILL_RUST_RATE', 'SKILL_RATES', 'SKILL_RUST_RATES'))
        for existingtoken in existingtokens:
            pydwarf.log.debug('Modifying arguments for existing token %s.' % existingtoken)
            edited = False
            if existingtoken.value in ('SKILL_RATES', 'SKILL_RUST_RATES'): needsnew = False
            editedtoken = edittoken(existingtoken, rates)
            editedtotal += editedtoken
            pydwarf.log.debug(('Modified arguments for token.') if editedtoken else ('Token already has no skill rust.'))
            
        # Add a new one if no token affecting all skills was found   
        if needsnew:
            pydwarf.log.debug('Adding new SKILL_RUST_RATES token.')
            creaturetoken.addprop('SKILL_RUST_RATES:NONE:NONE:NONE')
            
        # Creature already had no skill rust; consider this a failure
        elif not editedtotal:
            pydwarf.log.error('%s already has no skill rust.' % creaturetoken)
            failures.append(creaturetoken)
    
    # All done!
    failurecount = len(failures) + len(creatures) - len(creaturetokens)
    if failurecount == 0:
        return pydwarf.success('Removed skill rust from %d creatures.' % len(creatures))
    else:
        return pydwarf.failure('Failed to remove skill rust from %d creatures.' % failurecount)



def edittoken(token, rates):
    # Convenience method: Set a skill token's last three arguments to NONE:NONE:NONE. (This kills the rust.)
    if existingtoken.args[-4:-1] == rates:
        return False
    else:
        for i in xrange(1, 4): existingtoken.args[-i] = rates[i-1]
        return True
