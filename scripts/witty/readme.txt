Restricted Nobles created by Witty. (http://www.bay12forums.com/smf/index.php?topic=150702.0)
Restricted Nobles Ported to PyDwarf by Sophie Kirschner. (http://www.pineapplemachine.com)

How this works; 

I used the CREATURE_CLASS token to declare an arbitrary distinction (DWARF or GOBLIN, in this case) for the 
appropriate creature and then used the ALLOWED_CLASS (For Dwarf Only Nobles) or REJECTED_CLASS (Goblin Excluded Nobles)
to restrict the allowed nobility. 

All files changes are marked with a WM insignia. If you would like to remove the restriction to one of the noble positions
just find the position in the entity_default.txt and remove either the ALLOWED_CLASS or REJECTED_CLASS token for that position. 
Note all of this must be done before worldgen, and will have no effect if you make any changes during play. 
