# -*- coding: utf-8 -*-
import nest
import nest.topology as topp
import pylab

rowcol = 40
extent = [1.,1.]
model = 'iaf_neuron'


CD = {'connection_type':'divergent'}

CD1 = { 'connection_type': 'divergent', 
                'mask': {'circular':{'radius':0.25}}, 
                'kernel': {'uniform' : {'min': 0.6, 'max':0.8}},
                'weights': 2.,
                'delays': {'linear': {'c': 2., 'a':12.}}}	
                
CD2 =      {  'connection_type': 'divergent',
                'kernel': {'gaussian2D':{'p_center':1.,'sigma_x':0.25,'sigma_y':0.5,'cutoff':0.65}},
                'mask': {'circular':{'radius':0.5}} ,	# Why is mask circular here ?? Because 2d gaussian mask not available.
                'allow_oversized_mask':True
                }
                
CD3 =       { 'connection_type': 'divergent',
                'mask' : {'doughnut':{'inner_radius':0.25,'outer_radius':0.6}},
                'kernel': 0.5,
                'weights': {'linear':{'c':1.,'a':-1.}},	# How is c 1 ?? because with c ==1 in the middle, it becomes 0.75 at the beginning of the doughnut.
                'allow_oversized_mask':True}

CD4_local =       { 'connection_type': 'divergent',
                  'weights': 1.,
                'mask' : {'circular':{'radius':0.1}}}
CD4_lr1 =       { 'connection_type': 'divergent',
                  'weights': 1.2,
                'mask' : {'circular':{'radius':0.2},
                          'anchor': [0.43,0.25]}}
CD4_lr2 =       { 'connection_type': 'divergent',
                  'weights': 1.2,
                'mask' : {'circular':{'radius':0.2},
                          'anchor': [-0.43,0.25]}}
CD4_lr3 =       { 'connection_type': 'divergent',
                  'weights': 1.2,
                'mask' : {'circular':{'radius':0.2},
                          'anchor': [0.,-0.5]}}

def plot_layer_targets(cds,savename):
    nest.ResetKernel()
    layer = topp.CreateLayer({'rows':rowcol,'columns':rowcol,'extent':extent,'elements':model})
    for cd in cds:
        topp.ConnectLayers(layer,layer,cd)
    
    ctr = topp.FindCenterElement(layer)
    fig = topp.PlotLayer(layer,nodesize=20)
    topp.PlotTargets(ctr,layer,fig=fig,tgt_color='red')
    
    pylab.savefig('%s.png'%savename)
    pylab.close()

plot_layer_targets([CD1],'cd1')
plot_layer_targets([CD2],'cd2')
plot_layer_targets([CD3],'cd3')
#plot_layer_targets([CD4_local,CD4_lr1,CD4_lr2,CD4_lr3],'cd4')

