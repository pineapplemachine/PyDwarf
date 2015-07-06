import pydwarf
import raws



decay_dir = pydwarf.rel(__file__, 'hack/decay')



@pydwarf.urist(
    name = 'omniclasm.decay.starvingdead',
    version = '1.0.0',
    author = ('Omniclasm', 'Sophie Kirschner'),
    description = '''With this script running, all undead that have been on the map for a
        time (default: 1 month) start to gradually decay, losing strength, speed, and 
        toughness. After they have been on the map for even longer (default: 3 months),
        they collapse upon themselves, never to be reanimated.
    ''',
    arguments = {
        'start': 'Number of months before decay sets in.',
        'die': 'Number of months before collapsing entirely.',
        'auto_run': 'If set to True then the script will be started automatically upon startup.'
    },
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x)
)
def starvingdead(df, start=1, die=3, auto_run=True):
    return pydwarf.urist.getfn('pineapple.utils.addhack')(
        df,
        auto_run = 'starvingdead start %d %d' % (start, die) if auto_run is True else auto_run,
        loc = 'hack/scripts',
        path = pydwarf.rel(decay_dir, 'starvingdead.rb'),
        kind = raws.reffile
    )



@pydwarf.urist(
    name = 'omniclasm.decay.deteriorate.corpses',
    version = '1.0.0',
    author = ('Omniclasm', 'Sophie Kirschner'),
    description = '''In long running forts, especially evil biomes, you end up with a lot of
        toes, teeth, fingers, and limbs scattered all over the place. Various corpses from
        various sieges, stray kitten corpses, probably some heads. This script causes all of
        those to rot away into nothing after several months.
    ''',
    arguments = {
        'auto_run': 'If set to True then the script will be started automatically upon startup.'
    },
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x)
)
def deterioratecorpses(df, auto_run=True):
    return pydwarf.urist.getfn('pineapple.utils.addhack')(
        df,
        auto_run = 'deterioratecorpses start' if auto_run is True else auto_run,
        loc = 'hack/scripts',
        path = pydwarf.rel(decay_dir, 'deterioratecorpses.rb'),
        kind = raws.reffile
    )



@pydwarf.urist(
    name = 'omniclasm.decay.deteriorate.clothes',
    version = '1.0.0',
    author = ('Omniclasm', 'Sophie Kirschner'),
    description = '''This script is fairly straight forward. All of those slightly worn wool
        shoes that dwarves scatter all over the place will deteriorate at a greatly increased
        rate, and eventually just crumble into nothing. As warm and fuzzy as a dining room
        full of used socks makes your dwarves feel, your FPS does not like it.
    ''',
    arguments = {
        'auto_run': 'If set to True then the script will be started automatically upon startup.'
    },
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x)
)
def deteriorateclothes(df, auto_run=True):
    return pydwarf.urist.getfn('pineapple.utils.addhack')(
        df,
        auto_run = 'deteriorateclothes start' if auto_run is True else auto_run,
        loc = 'hack/scripts',
        path = pydwarf.rel(decay_dir, 'deteriorateclothes.rb'),
        kind = raws.reffile
    )



@pydwarf.urist(
    name = 'omniclasm.decay.deteriorate.food',
    version = '1.0.0',
    author = ('Omniclasm', 'Sophie Kirschner'),
    description = '''With this script running, all food and plants wear out and disappear after
        several months. Barrels and stockpiles will keep them from rotting, but it won't keep
        them from decaying.
    ''',
    arguments = {
        'auto_run': 'If set to True then the script will be started automatically upon startup.'
    },
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x)
)
def deterioratefood(df, auto_run=True):
    return pydwarf.urist.getfn('pineapple.utils.addhack')(
        df,
        auto_run = 'deterioratefood start' if auto_run is True else auto_run,
        loc = 'hack/scripts',
        path = pydwarf.rel(decay_dir, 'deterioratefood.rb'),
        kind = raws.reffile
    )
