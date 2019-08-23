﻿import numpy as np
import pylab
import nest

"""
Setting up NEST
"""
nest.ResetKernel()
np.random.seed()
rndSeeds = np.random.randint(0, 1000, 2)
rngSeeds = [rndSeeds[0]]
grngSeed = rndSeeds[1]
dt = .1
nest.SetStatus([0],{"resolution"        : dt,
                    "rng_seeds"         : rngSeeds,
                    "grng_seed"         : grngSeed})

"""
Simulation parameters
"""
simtime = 10000.
wuptime = 400.

"""
Network parameters
"""
mode        = "broad_both"           # select between: broad_in, broad_out, broad_both in the connectivity section
N           = 1000                 # number of neurons
epsilon     = .2                   # connection probability
C           = int(epsilon * N)     # number of pre/post synaptic neurons
ri          = 100                  # number of neurons to record from
je          = 1.                   # weight of external input
g           = 10                   # strength ratio inh-exc
ji          = -je * g              # inhibitory weights
delay_ii    = 2.
delay_ext    = 1.

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

"""
External input
"""
ext = nest.Create("dc_generator", params={"amplitude":13.})

"""
Recorders
"""
recorder_params = {"start"        : wuptime,
                   "to_file"     : False,
                   "to_memory"   : True}
sd_i = nest.Create("spike_detector", params=recorder_params)
vm_i = nest.Create("voltmeter", params=recorder_params)

"""
Create neurons
"""
inh = nest.Create(neuron_model, N, params=neuron_params)

"""
Connect neurons

Write your code here
--------------------
Implement different connectivity schemes as indicated in 
the exercise sheet. Start with fixing the out-degree and then do the same 
with the in-degree. Finally just make both broader. Write your code such that 
you can switch easily from one option to the other, usung the mode parameter
specified in the Network Parameters section. Look in the exercise sheet 
for hints if you need.
"""
syn_dict = {"weight": ji, "delay": delay_ii}

if mode == "broad_in":
    conn_dict = {"rule": "fixed_indegree", "indegree":C}
elif mode == "broad_out":
    conn_dict = {"rule": "fixed_outdegree", "outdegree": C}
elif mode == "broad_both":
    conn_dict = {"rule": "pairwise_bernoulli", "p":epsilon}
else:
    print("you moron")

nest.Connect(inh, inh, conn_dict, syn_dict)


"""
Connect external drive
"""
nest.Connect(ext, inh, "all_to_all",
             syn_spec={"weight":je, "delay":delay_ext})

"""
Connect to recorders
"""
nest.Connect(inh, sd_i, "all_to_all",
             syn_spec={"weight":1.0, "delay":1.0})

nest.Connect(vm_i, inh[:ri], "all_to_all",
             syn_spec={"weight":1.0, "delay":1.0})
                      


"""
Simulate
"""
nest.Simulate(wuptime + simtime)

"""
Get data from recorders
ti: a list of all firing times
si: a list of the corresponding neuron ids
pvi: a list of all recorded membrane potentials
tvi: a list of the corresponding recording times
svi: a list of the corresponding neuron ids
"""
data_si = nest.GetStatus(sd_i, "events")[0]
si, ti = data_si["senders"], data_si["times"]

data_vi = nest.GetStatus(vm_i, "events")[0]
svi, tvi, pvi = np.array(data_vi["senders"]), np.array(data_vi["times"]), np.array(data_vi["V_m"])


"""
Plot membrane potential trace (recorder neurons gray + average in blue)

Write your code here
--------------------
Write a function or a just a piece of code that plots the membrane traces of the
recorded neurons in gray. Calculate the average and plot it in a different color.
Please note that svi,tvi,pvi have been already converted into numpy arrays.

"""
def plot_V_m(tvi, pvi):
    num_to_plot = 10  # plot just ten neurons
    selected = np.random.choice(np.arange(0,ri), num_to_plot)
    fig, axes = pylab.subplots(nrows=num_to_plot + 1, ncols=1)
    pvi_array = np.reshape(pvi, (-1,ri))[:,selected] #dim: (neuronindex, time)
    tvi_array = np.reshape(tvi, (-1,ri)) # recording time is same for all neurons (repetitive) so don't care
    for index in range(num_to_plot):
        axes[index].plot(tvi[::ri], pvi_array[:,index], "gray")
    axes[-1].plot(tvi[::ri], np.mean(pvi_array,axis=1), "blue") # plot the avg.

pylab.figure()
plot_V_m(tvi=tvi, pvi=pvi)

pylab.xlabel("time(ms)", fontsize=30)
pylab.ylabel("potential(mV)", fontsize=30)






"""
Plot rate histogram

Write your code here
--------------------

Calculate the number of spikes emitted by each neuron and store
results in a rate vector, which you can then apply hist to
"""
def plot_rate_hist(ti,si):
    num_to_plot = 10  # plot just ten neurons
    selected = np.random.choice(np.arange(0, N), num_to_plot)

    ids_unique, freq_ids = np.unique(si, return_counts=True) #id of neurons, num. of spikes for each neuron
    avg_firingrates = freq_ids[selected] / simtime
    pylab.hist(avg_firingrates)

    # for index in range(num_to_plot):
    #     axes[index].plot(ti_array[:,index], si_array[:,index],"blue")

pylab.figure()
plot_rate_hist(ti=ti, si=si)

pylab.xlabel("rate [spks]", fontsize=30)
pylab.ylabel("counts", fontsize=30)


"""
Bonus: Plot raster plot ordered by rate

Write your code here
--------------------

Use the rate vector calculated in the previous exercise to sort the spiking data
such that neurons with a higher firing rate are plotted above neurons with a
lower firing rate.

"""
#Uncomment the following section to do the bonus analysis
#pylab.figure()

#pylab.xlabel("time(ms)", fontsize=30)
#pylab.ylabel("neuron id", fontsize=30)



pylab.show()
