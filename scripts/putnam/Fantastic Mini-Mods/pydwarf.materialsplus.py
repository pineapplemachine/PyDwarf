import os
import pydwarf
from raws import rawsfile, rawstoken

permitted_reactions = '''       
\t[PERMITTED_REACTION:MANGANESE_STEEL_MAKING_BARS]
\t[PERMITTED_REACTION:MANGANESE_STEEL_MAKING_ORE]
\t[PERMITTED_REACTION:HIGH_SPEED_STEEL_MAKING]
\t[PERMITTED_REACTION:BERYLLIUM_MACRO_PUTNAM]
\t[PERMITTED_REACTION:KROLL_MACRO_PUTNAM]
\t[PERMITTED_REACTION:BERYLLIUM_REFINING_PUTNAM_GEMS]
\t[PERMITTED_REACTION:BERYLLIUM_REFINING_PUTNAM_BOULDER]
\t[PERMITTED_REACTION:MAKE_SULFURIC_ACID_PUTNAM]
\t[PERMITTED_REACTION:KROLL_PROCESS_BOULDER_PUTNAM]
\t[PERMITTED_REACTION:KROLL_PROCESS_GEM_PUTNAM]
\t[PERMITTED_REACTION:PIDGEON_PROCESS_PUTNAM]'''

# Utility function for putting new properties after an inorganic's USE_MATERIAL_TEMPLATE token, if it has one
# Otherwise, the property is just added after the INORGANIC object token.
def addaftertemplate(inorganic, addition):
    template = inorganic.getuntil(exact_value='USE_MATERIAL_TEMPLATE', until_exact_value='INORGANIC')
    addafter = template if template else inorganic
    return addafter.add(addition)

@pydwarf.urist(
    name = 'materials plus',
    version = 'alpha',
    author = ('Putnam', 'Sophie Kirschner'),
    description = 'Adds a bunch of materials to the game.',
    compatibility = (pydwarf.df_0_34, pydwarf.df_0_40)
)
def materialsplus(raws):
    exceptions = 0
    
    try:
        for zircon in raws.all(exact_value='INORGANIC', re_args=['.* ZIRCON']):
            addaftertemplate(zircon, 'MATERIAL_REACTION_PRODUCT:KROLL_PROCESS:INORGANIC:ZIRCONIUM_PUTNAM')
        pydwarf.log.debug('Added reaction to zircons.')
    except:
        pydwarf.log.exception('Failed to add reaction to zircons.')
        exceptions += 1
        
    try:
        for beryl in raws.all(exact_value='INORGANIC', re_args=['.* BERYL|HELIODOR|MORGANITE|GOSHENITE|EMERALD']):
            addaftertemplate(beryl, 'REACTION_CLASS:BERYLLIUM')
        pydwarf.log.debug('Added reaction to beryls.')
    except:
        pydwarf.log.exception('Failed to add reaction to beryls.')
        exceptions += 1
    
    try:
        chromite = raws.get('INORGANIC:CHROMITE')
        pyrolusite = raws.get('INORGANIC:PYROLUSITE')
        addaftertemplate(chromite, '[METAL_ORE:CHROMIUM_PUTNAM:100][METAL_ORE:IRON:50]')
        addaftertemplate(pyrolusite, 'METAL_ORE:MANGANESE_PUTNAM:100')
        pydwarf.log.debug('Added titanium ores.')
    except:
        pydwarf.log.exception('Failed to add titanium ores.')
        exceptions += 1
    
    try:
        for silicon in raws.all(exact_value='INORGANIC', re_args=['ANDESITE|OLIVINE|HORNBLENDE|SERPENTINE|ORTHOCLASE|MICROCLINE|MICA']):
            addaftertemplate(silicon, 'REACTION_CLASS:SILICON')
        pydwarf.log.debug('Added silicon reactions.')
    except:
        pydwarf.log.exception('Failed to add silicon reactions.')
        exceptions += 1
        
    try:
        dolomite = raws.get('INORGANIC:DOLOMITE')
        addaftertemplate(dolomite, 'REACTION_CLASS:PIDGEON_PROCESS')
        pydwarf.log.debug('Added reaction to dolomite.')
    except:
        pydwarf.log.exception('Failed to add reaction to dolomite.')
        exceptions += 1
        
    try:
        raws.get('ENTITY:MOUNTAIN').get(exact_value='PERMITTED_REACTION').add(permitted_reactions, reverse=True)
        pydwarf.log.debug('Added permitted reactions.')
    except:
        pydwarf.log.exception('Failed to add permitted reactions.')
        exceptions += 1
    
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Materials Plus')):
        for filename in files:
            suffix = '_mat_plus.txt'
            if filename.endswith(suffix):
                path = os.path.join(root, filename)
                destname = 'putnam_%s' % filename[:-len(suffix)]
                rfile = raws.getfile(destname)
                if rfile:
                    pydwarf.log.debug('Appending data to file %s from %s...' % (destname, path))
                    with open(path, 'rb') as matplus: rfile.add(matplus)
                else:
                    with open(path, 'rb') as matplus: raws.addfile(rfile=rawsfile(header=destname, rfile=matplus))
                    pydwarf.log.debug('Adding data to new file %s.' % destname)
                    
    if exceptions == 0:
        return pydwarf.success()
    else:
        return pydwarf.failure('Failed to complete %d operations.' % exceptions)
