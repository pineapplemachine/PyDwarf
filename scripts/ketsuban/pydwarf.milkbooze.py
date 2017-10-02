import pydwarf
import raws

milk_beer_reaction = """
[REACTION:BREW_DRINK_FROM_ANIMAL_EXTRACT]
    [NAME:brew drink from animal extract]
    [BUILDING:STILL:CUSTOM_A]
    [REAGENT:extract:150:LIQUID_MISC:NONE:NONE:NONE]
        [HAS_MATERIAL_REACTION_PRODUCT:DRINK_MAT]
        [UNROTTEN]
    [REAGENT:extract container:1:NONE:NONE:NONE:NONE]
        [CONTAINS:extract]
    [REAGENT:barrel/pot:1:NONE:NONE:NONE:NONE]
        [EMPTY]
        [FOOD_STORAGE_CONTAINER] barrel or any non-absorbing tool with FOOD_STORAGE
        [PRESERVE_REAGENT]
        [DOES_NOT_DETERMINE_PRODUCT_AMOUNT]
    [PRODUCT:100:5:DRINK:NONE:GET_MATERIAL_FROM_REAGENT:extract:DRINK_MAT]
        [PRODUCT_TO_CONTAINER:barrel/pot]
        [PRODUCT_DIMENSION:150]
    [SKILL:BREWING]
"""

milk_beer_material_template = """
        [USE_MATERIAL_TEMPLATE:MILK_BEER:CREATURE_ALCOHOL_TEMPLATE]
            [STATE_NAME:ALL_SOLID:frozen %(adj)s milk beer]
            [STATE_ADJ:ALL_SOLID:frozen %(adj)s milk beer]
            [STATE_NAME:LIQUID:%(adj)s milk beer]
            [STATE_ADJ:LIQUID:%(adj)s milk beer]
            [STATE_NAME:GAS:boiling %(adj)s milk beer]
            [STATE_ADJ:GAS:boiling %(adj)s milk beer]
            [PREFIX:NONE]
            [MULTIPLY_VALUE:2]"""

@pydwarf.urist(
    name = 'ketsuban.milkbooze',
    title = 'Milk Booze',
    version = '1.0.0',
    author = 'Ketsuban',
    description = '''Adds reactions which allow the brewing of alcoholic drinks
        from animal milk.
        Based on http://www.bay12forums.com/smf/index.php?topic=167546.0''',
    arguments = {
        'entities': '''The entities which should be allowed to brew the new drinks.
            Defaults to only dwarves.'''
    }
)
def milkbooze(df, entities=["MOUNTAIN"]):
    # Add material templates to milkable creatures
    beers_added = 0
    for file in df.files.values():
        if file.name.startswith("creature_"):
            last_name_token = None
            last_caste_token = None
            for token in file.tokens():
                if token.value == "CASTE":
                    last_caste_token = token
                elif token.value == "NAME":
                    last_name_token = token
                elif(
                    last_caste_token and
                    last_name_token and
                    token.next and
                    token.value == "USE_MATERIAL_TEMPLATE" and
                    token.args[0] == "MILK" and
                    token.args[1] == "MILK_TEMPLATE"
                ):
                    adjective = last_name_token.args[-1]
                    last_caste_token.addafter(
                        milk_beer_material_template % {"adj": adjective}
                    )
                    beers_added = beers_added + 1
                    pydwarf.log.debug("Added %s milk beer material template." % adjective)
    # Add MATERIAL_REACTION to milk template
    for cheese in df.all(
        "MATERIAL_REACTION_PRODUCT:CHEESE_MAT:LOCAL_CREATURE_MAT:CHEESE"
    ):
        pydwarf.log.debug(
            "Adding a milk beer material reaction product inside file %s." % str(cheese.file)
        )
        cheese.addafter(
            "[MATERIAL_REACTION_PRODUCT:DRINK_MAT:LOCAL_CREATURE_MAT:MILK_BEER]"
        )
    # Add a new reaction to stills to produce milk beers,
    # and give the specified entities access to that reaction
    addobject = pydwarf.scripts.pineapple.utils.addobject(
        df,
        add_to_file="raw/objects/reaction_milk_beer.txt",
        tokens=milk_beer_reaction,
        permit_entities=entities
    )
    if not addobject:
        return addobject
    else:
        return pydwarf.success("Added milk beers to %d milkable creatures." % beers_added)
