#!/usr/bin/env python
# coding: utf-8

import queryableadd
import queryableprop



class queryableaddprop(queryableadd.queryableadd, queryableprop.queryableprop):
    
    # Inheriting classes must implement a propterminationfilter method and an add method
    
    # TODO: move this into objects module or something
    add_props_before_default = tuple()
    add_props_after_default = ('COPY_TAGS_FROM',)
    add_props_before_after_default = (add_props_before_default, add_props_after_default)
    add_props_before_after = {
        'CREATURE': (
            add_props_before_default + ('CASTE', 'SELECT_CASTE', 'SELECT_MATERIAL', 'SELECT_TISSUE', 'SELECT_TISSUE_LAYER'),
            add_props_after_default + ('APPLY_CREATURE_VARIATION', 'APPLY_CURRENT_CREATURE_VARIATION', 'CV_REMOVE_TAG', 'CV_ADD_TAG', 'GO_TO_END', 'GO_TO_START', 'GO_TO_TAG'),
        ),
        'INORGANIC': (
            add_props_before_default,
            add_props_after_default + ('USE_MATERIAL_TEMPLATE',),
        ),
    }
    
    def addprop(self, *args, **kwargs):
        beforevalues, aftervalues = (
            queryableaddprop.add_props_before_after.get(
                self.value, queryableaddprop.add_props_before_after_default
            )
        )
        addafter = self.lastprop(value_in=aftervalues, until_value_in=beforevalues)
        if addafter is None: addafter = self
        addafter.add(*args, **kwargs)
            
    def setprop(self, *args, **kwargs):
        self.setsingular(self.getprop, self.addprop, *args, **kwargs)
        
    def setlastprop(self, *args, **kwargs):
        self.setsingular(self.lastprop, self.addprop, *args, **kwargs)
        
    def setallprop(self, *args, **kwargs):
        self.setplural(self.allprop, *args, **kwargs)
