
import numpy as np
import random as rand
import pylab as pl
import nest
import nest.topology as topo
import matplotlib.pylab as plt

from helper_functions import *
"""
Setting up NEST
"""
nest.ResetKernel()
np.random.seed()
rndSeeds = np.random.randint(0, 1000, 2)
rngSeeds = [rndSeeds[0]]
grngSeed = rndSeeds[1]
dt = .1
nest.SetStatus([0], {"resolution"        : dt,
                     "rng_seeds"         : rngSeeds,
                     "grng_seed"         : grngSeed,
                     'print_time':True})

"""
Simulation parameters
"""
simtime = 1000.
wuptime = 200.


"""
You may want to use these variables to alternate between the different 
configurations. You need long simualtions to stimate correlation coefficients
properly.
"""
import sys
gauss_ex = sys.argv[1]=='True'
gauss_in = sys.argv[2]=='True'


"""
Network parameters
"""
order   = 1000
ne      = 4 * order
ni      = 1 * order
epsilon = .1
je      = .1
g       = 10
ji      = -g * je
delay   = 1.5

#topology parameters
extentX = 1.
extentY = 1.
wrapped = True

#layer parameters
layer_dict = {"extent"      : [extentX, extentY],
              "edge_wrap"   : wrapped}

#connection parameters

"""
Write your code here
--------------------

Write the dictionaries that you will use to connect the neurons locally. You can
use one dictionary for both populations if you wish. Remember that your choice 
of parameters has to match the description given in the exercise sheet. Number
of connections have to be roughly the same as in the random case. Use the
function GetConnections() to find out whether you are making the same number of
connections or not.
"""
sigma=0.127
condict_gauss_ex_ex = {'connection_type': 'divergent',
              'mask':{'circular':{'radius':3*sigma}},
              'kernel': {'gaussian': {'p_center': 1.0, 'sigma': sigma}},
              'weights':je,
              'delays':1.5,
            "number_of_connections": int(epsilon*ne),
              }

condict_gauss_ex_in = {'connection_type': 'divergent',
              'mask':{'circular':{'radius':3*sigma}},
              'kernel': {'gaussian': {'p_center': 1.0, 'sigma': sigma}},
              'weights':je,
              'delays':1.5,
            "number_of_connections": int(epsilon*ni),
              }



condict_gauss_in_ex = {'connection_type': 'divergent',
              'mask': {'circular': {'radius': 3 * sigma}},
              'kernel':{'gaussian':{'p_center':1.0,'sigma':sigma}},
              'weights':ji,
              'delays':1.5,
            "number_of_connections": int(epsilon*ne),
              }
condict_gauss_in_in = {'connection_type': 'divergent',
              'mask': {'circular': {'radius': 3 * sigma}},
              'kernel':{'gaussian':{'p_center':1.0,'sigma':sigma}},
              'weights':ji,
              'delays':1.5,
            "number_of_connections": int(epsilon*ni),
              }



condict_rand_ex_ex = {"rule": "fixed_outdegree", "outdegree": int(epsilon*ne)}
condict_rand_ex_in = {"rule": "fixed_outdegree", "outdegree": int(epsilon*ni)}
condict_rand_in_ex = {"rule": "fixed_outdegree", "outdegree": int(epsilon*ne)}
condict_rand_in_in = {"rule": "fixed_outdegree", "outdegree": int(epsilon*ni)}



"""
Neuron parameters
"""
neuron_model= "iaf_psc_alpha"
tauSynEx    = .5
tauSynIn    = .5
tauMem      = 20.
theta       = 20.
reset       = .0
neuron_params= {"C_m"       : 1.,
                "tau_m"     : tauMem,
                "tau_syn_ex": tauSynEx,
                "tau_syn_in": tauSynIn,
                "t_ref"     : 2.,
                "E_L"       : .0,
                "V_m"       : .0,
                "V_reset"   : reset,
                "V_th"      : theta}


nest.CopyModel("iaf_psc_alpha", "exc", params=neuron_params)
nest.CopyModel("iaf_psc_alpha", "inh", params=neuron_params)

"""
Part a:
Create layers

The following code distributes the neurons randomly across the layer.
"""

ex_pos = [[np.random.uniform(-extentX / 2., extentX / 2.),\
           np.random.uniform(-extentY / 2., extentY / 2.)] for j in xrange(ne)]
layer_dict.update({"positions": ex_pos,"elements":"exc"})
excNeurons=topo.CreateLayer(layer_dict)

in_pos = [[np.random.uniform(-extentX / 2., extentX / 2.),\
           np.random.uniform(-extentY / 2., extentY / 2.)] for j in xrange(ni)]
layer_dict.update({"positions": in_pos, "elements":"inh"})
inhNeurons=topo.CreateLayer(layer_dict)

"""
Write your code here
--------------------
Create a layer of inhibitory neurons and another of excitatory neurons. Use
the funcion topo.CreateLayer() for that.
"""

"""
Part b:
Connect the layers
"""
if gauss_ex:
    topo.ConnectLayers(excNeurons,inhNeurons,condict_gauss_ex_in)
    topo.ConnectLayers(excNeurons, excNeurons, condict_gauss_ex_ex)
    conn_ex_ex = condict_gauss_ex_ex
    conn_ex_in = condict_gauss_ex_in
else:
    nest.Connect(nest.GetLeaves(excNeurons)[0],nest.GetLeaves(excNeurons)[0],conn_spec=condict_rand_ex_ex,syn_spec={'weight':je,'delay':delay})
    nest.Connect(nest.GetLeaves(excNeurons)[0],nest.GetLeaves(inhNeurons)[0],conn_spec=condict_rand_ex_in,syn_spec={'weight':je,'delay':delay})
    conn_ex_ex = condict_rand_ex_ex
    conn_ex_in = condict_rand_ex_in


if gauss_in:

    topo.ConnectLayers(inhNeurons,inhNeurons,condict_gauss_in_in)
    topo.ConnectLayers(inhNeurons, excNeurons, condict_gauss_in_ex)
    conn_in_in = condict_gauss_in_in
    conn_in_ex = condict_gauss_in_ex

else:
    nest.Connect(nest.GetLeaves(inhNeurons)[0],nest.GetLeaves(excNeurons)[0],conn_spec=condict_rand_in_ex,syn_spec={'weight':ji,'delay':delay})
    nest.Connect(nest.GetLeaves(inhNeurons)[0],nest.GetLeaves(inhNeurons)[0],conn_spec=condict_rand_in_in,syn_spec={'weight':ji,'delay':delay})
    conn_in_in = condict_rand_in_in
    conn_in_ex = condict_rand_in_ex


print len(nest.GetConnections(nest.GetLeaves(inhNeurons)[0]))/len(nest.GetLeaves(inhNeurons)[0])
print len(nest.GetConnections(nest.GetLeaves(excNeurons)[0]))/len(nest.GetLeaves(excNeurons)[0])


"""
Write your code here
--------------------

Connect the layers (EE,EI,IE,II). Write your code in such a way that you can 
easily switch between random and local connectivity.
"""

"""
External input
"""
ext_rate=7.8
ext = nest.Create("poisson_generator",params={"rate":ext_rate*1e3})

"""
Recorders
"""
recorder_params    ={"start"        : wuptime,
                      "to_file"     : False,
                      "to_memory"   : True}
sd = nest.Create("spike_detector", params=recorder_params)
vm = nest.Create("voltmeter", params=recorder_params)

"""
Connect external drive
"""
nest.Connect(ext, nest.GetLeaves(inhNeurons)[0] + nest.GetLeaves(excNeurons)[0], "all_to_all",
             syn_spec={"weight":je, "delay":1.})
             

"""
Connect to recorders
"""
nest.Connect(nest.GetLeaves(excNeurons)[0], sd)
            
nest.Connect(vm,nest.GetLeaves(excNeurons)[0][0:10])
             


"""
Part b cont:
Plot the network
"""
def plot_layer_targets(cds, savename):
    layer = topo.CreateLayer(layer_dict)
    for cd in cds:
        topo.ConnectLayers(layer, layer, cd)

    ctr = topo.FindCenterElement(layer)
    fig = topo.PlotLayer(layer, nodesize=20)
    topo.PlotTargets(ctr, layer, fig=fig, tgt_color="red")

    plt.savefig("%s.png" % savename)
    plt.close()

#test to see if kernel is correct
if gauss_ex and gauss_in:
	plot_layer_targets([conn_ex_ex], "ex-ex")
	plot_layer_targets([conn_ex_in], "ex-in")
	plot_layer_targets([conn_in_ex], "in-ex")
	plot_layer_targets([conn_in_in], "in-in")
"""
Write your code here
--------------------

Plot the network connectivity. Re-use the function provided in 
exercise 2.
"""

"""
Simulate
"""
nest.Simulate(wuptime + simtime)

"""
Get data from recorders
"""
data_sd = nest.GetStatus(sd, "events")[0]
s_sd,t_sd = data_sd["senders"], data_sd["times"]

data_v = nest.GetStatus(vm, "events")[0]
s_v,t_v,p_v = np.array(data_v["senders"]), np.array(data_v["times"]), np.array(data_v["V_m"])

"""
Part c:
Analyse the data
"""

"""
Write your code here
--------------------

Plot the spiking activity and the PSTH. Re-use the code that you implemented in 
previous exercises.
"""
name=''
if gauss_ex:
    name+='ex'
if gauss_in:
    name+='in'

plt.figure(figsize=(16,10))
#plt.xlim([2000,2500])
plt.plot(t_sd,s_sd,'.',markersize=3)
plt.savefig('activity'+name+'.png')


plt.figure(figsize=(16,10))
plot_rate_sorted(s_sd,t_sd)
plt.savefig('activityrate__sorted'+name+'.png')

plt.figure(figsize=(16,10))
count_vector=np.bincount(s_sd)
plot_rate_histogram(count_vector,simtime)
plt.savefig('histogram'+name+'.png')

def get_ccs(times, senders, n_sample=1000, bin_size=5.):
    unique_ids = np.unique(senders)
    bins= np.arange(wuptime, simtime + wuptime + bin_size, bin_size)
    cc = np.zeros(n_sample)
    for i in xrange(n_sample):
        sp1, sp2 = rand.sample(unique_ids, 2)
        psth1 = np.histogram(times[senders == sp1], bins)[0]
        psth2 = np.histogram(times[senders == sp2], bins)[0]
        cc[i] = np.corrcoef(psth1, psth2)[0][1]
    return cc

plt.figure(figsize=(16,10))
cc=get_ccs(t_sd, s_sd,n_sample=20000)
plt.hist(cc,np.arange(-1,1,0.01))
plt.xlabel("correlation coefficient", fontsize=30)
plt.ylabel("counts", fontsize=30)
plt.title('CC mean {}'.format(np.mean(cc)))
plt.savefig('cc_histogram'+name+'.png')

