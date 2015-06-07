import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pydwarf
import shukaroutils

forgedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creationforge')

@pydwarf.urist(
    name = 'shukaro.creationforge',
    version = '1.0.0',
    author = ('Shukaro', 'Sophie Kirschner'),
    description = '''This is a simple workshop I modded in to help test custom reactions,
        buildings, and creatures. It's used to create various different items so that you
        don't have to set up an entire fortress to test some reactions. Hopefully it's a
        useful tool to people, even if it's just to look at the raw formatting. ''',
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x)
)
def higherlearning(dfraws, entities=shukaroutils.default_entities):
    return shukaroutils.addraws(pydwarf, dfraws, forgedir, entities)
