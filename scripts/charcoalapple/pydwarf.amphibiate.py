import pydwarf
import raws
import os

#base_dir = '/Applications/Lazy Mac Pack v0.47.03 dfhack-a0/'
#df = raws.dir(base_dir+'df_osx v0.47.03/')

base_dir = '/Applications/Lazy Mac Pack v0.47.04 dfhack-b1/'
df = raws.dir(base_dir+'df_osx v0.47.04/')
#overridden by config.yaml

tea_dir = pydwarf.rel(__file__, 'raw/tea')
default_entities="MOUNTAIN"


@pydwarf.urist(
    name = 'charcoalapple.amphibiate',
    title = 'Flytrap',
    version = '1.0.0',
    author = 'Adam Willats',
    description = 'Turns all [AQUATIC] animal people into [AMPHIBIOUS] creatures to make more stuff playable',
    #arguments  = {},
    #compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)

def amphibiate(df):
    animal_peeps = df.allobj('CREATURE',re_id='.+_MAN')
    #.each(lambda token: token.get('AQUATIC'))

    #doesn't work because people derive aquatic from base creature
    aquamen = animal_peeps.all('AQUATIC').each(lambda token: token.setvalue('AMPHIBIOUS'))

    #animal_peeps = df.allobj('CREATURE',re_id='.+_MAN')


    """
    for peep in animal_peeps:
        print peep.get('NAME')
        print peep
        #print peep.get('CREATURE') #gets the subsequent creature!
    """
    #aquats.each(lambda token: token.get('AQUATIC'))

    for aq in animal_peeps:
        #aq.removeprop('AQUATIC')
        #if corresponding creature is aquatic, add amphibious?
        print aq.get('NAME')

        try:
            aq.get('APPLY_CREATURE_VARIATION:ANIMAL_PERSON').add('AMPHIBIOUS')
        except:
            print 'this one, isnt an animal person'

    return pydwarf.success()


    """

    # does work! but doesn't return much useful stuff
    aquamen = df.all('AQUATIC').each(lambda token: token.setvalue('AMPHIBIOUS'))
    walkers = df.all('IMMOBILE_LAND').each(lambda token: token.remove())

    print('\n...\n')
    for aq in aquamen:
        print aq.get('NAME')




if aq.getprop('AQUATIC'):
    #print aq.get('NAME')
    #faq = aq.getprop('AQUATIC')
    aq.add('FABULOUS')
#aq.remove('AQUATIC')
"""

"""
pydwarf.urist.getfn('pineapple.utils.objecttokens')(
df,
object_type = 'CREATURE',
token = 'AQUATIC',
add_to = None,
remove_from = aquats
)

pydwarf.urist.getfn('pineapple.utils.objecttokens')(
df,
object_type = 'CREATURE',
token = 'IMMOBILE_LAND',
add_to = None,
remove_from = aquats
)

pydwarf.urist.getfn('pineapple.utils.objecttokens')(
df,
object_type = 'CREATURE',
token = 'AMPHIBIOUS',
add_to = aquats,
remove_from = None
)
"""
