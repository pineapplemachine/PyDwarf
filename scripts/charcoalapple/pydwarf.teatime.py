import pydwarf
import raws
import os

#base_dir = '/Applications/Lazy Mac Pack v0.47.03 dfhack-a0/'
#df = raws.dir(base_dir+'df_osx v0.47.03/')

base_dir = '/Applications/Lazy Mac Pack v0.47.04 dfhack-b1/'
df = raws.dir(base_dir+'df_osx v0.47.04/')

tea_dir = pydwarf.rel(__file__, 'raw/tea')
default_entities="MOUNTAIN"

#equivalent:
# aquifers = df.all('AQUIFER')
# aquifers = df.query(lambda token: token.value == 'AQUIFER')
#print len(df.all('AQUIFER'))
#for aquifer in aquifers: aquifer.remove()
#print len(df.all('AQUIFER'))

#need to get creatures first
#headers = df.query(lambda token: token == 'OBJECT:CREATURE')
#then from those, select dwarves
#dwarves = headers.each(lambda token: token.get('CREATURE:DWARF'))

@pydwarf.urist(
    name = 'charcoalapple.teatime',
    title = 'Flytrap',
    version = '1.0.0',
    author = 'Adam Willats',
    description = 'Makes tea (camellia sinensis) brewable!',
)

def add_tea(df, entities=default_entities):

    return pydwarf.urist.getfn('pineapple.easypatch')(
    df,
    files=tea_dir,
    loc='raw/objects',
    permit_entities=entities #no idea what this does
    )


#ANYTHING below here won't get called by default
"""
def get_boozy(df):
    plants = df.allobj('PLANT')

    boozeNames = []
    for plant in plants:
        #print plant.getprop('SEED')
        if plant.get('DRINK'):
            print "\ndrinkable:"
            print plant.get("NAME")

        #if plant.get('USE_MATERIAL_TEMPLATE:DRINK:PLANT_ALCOHOL_TEMPLATE'):
            #if plant.all("DRINK"):

            plantTokens_ = plant.tokens()

            for token in plantTokens_:
                args = token.args
                for arg in args:
                    if "LIQUID" in arg:
                        #print token.value
                        #print token.args
                        print token.args[1:]
                        #print token.get('LIQUID')
            print "done"

    return pydwarf.success()

def make_tea_brewable(df):
    #currently i'm rewriting tea trees as TEA_BREWABLE
    #but i'd like to use a script to add brewable properties to existing tea class
    return pydwarf.failure()

"""
#def query(self, filters, tokens=None, iter=False, **kwargs):
