import os
import pydwarf

greendir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raws/greensteel')

@pydwarf.urist(
    name = 'pineapple.greensteel',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = '''Adds an alloy which is lighter and sharper than steel but not so much
        as adamantine. It can be made from similar ingredients as steel with the addition
        of adamantine bars or a new adamant ore.''',
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def greensteel(df):
    # Add greensteel raws
    try:
        df.read(path=greendir, log=pydwarf.log)
        return pydwarf.success()
    except:
        pydwarf.log.exception('Failed to add greensteel raws.')
        return pydwarf.failure()
