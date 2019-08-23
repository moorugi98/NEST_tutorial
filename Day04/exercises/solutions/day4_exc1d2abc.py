import nest
import numpy as np
import matplotlib.pyplot as plt # needed for plotting

C  = 125
CE = int(0.8*C)
CI = int(0.2*C)

rate   = 10.0
nu_ext =  5.0

g     = -5.0
w_exc = 70.0
w_inh = g*w_exc

alpha = 1.1 # results in firing rate of 8.5 to 9 Hz

mus = np.arange(0.0,1.1,0.05)
weight_dists = []
for mu in mus:

    nest.ResetKernel()

    neuron = nest.Create('iaf_psc_alpha',1,{'tau_minus': 20.0})

    pg_exc = nest.Create('poisson_generator',1,{'rate': rate})
    inputs = nest.Create('parrot_neuron',CE)

    pg_inh = nest.Create('poisson_generator',1,{'rate': CI*rate})
    pg_ext = nest.Create('poisson_generator',1,{'rate': CE*nu_ext})

    # record spikes of neuron
    sd_post = nest.Create('spike_detector',1,{'to_file':   False,
                                              'to_memory': True})

    nest.SetDefaults('stdp_synapse',{'tau_plus': 20.0,
                                     'mu_plus':  mu,
                                     'mu_minus': mu,
                                     'alpha':    alpha,
                                     'lambda':   0.1,
                                     'Wmax':     2.0*w_exc})

    nest.Connect(pg_exc,inputs,syn_spec={'model':'static_synapse','weight':1.0,'delay':1.0})
    nest.Connect(inputs,neuron,syn_spec={'model':'stdp_synapse','weight':w_exc})
    nest.Connect(pg_inh,neuron,syn_spec={'model':'static_synapse','weight':w_inh})
    nest.Connect(pg_ext,neuron,syn_spec={'model':'static_synapse','weight':w_exc})
    nest.Connect(neuron,sd_post)

    nest.Simulate(100000.0)

    # simulate 100 s, determine weight distribution
    connections = nest.GetConnections(inputs)
    weights = np.array(nest.GetStatus(connections,'weight'))
    sim_time = 100000.0
    rec_step =   1000.0 # record weights in steps of 1 s
    for t in np.arange(rec_step,sim_time+rec_step,rec_step):
        nest.Simulate(rec_step)
        connections = nest.GetConnections(inputs)
        weights = np.append(weights,nest.GetStatus(connections,'weight'))

    weight_dists.append(np.histogram(weights,bins=50,range=[0.0,2.0*w_exc],normed=True)[0])

weight_dists = np.array(weight_dists).T

# plot weight dists
plt.figure(1)
plt.pcolor(mus,np.arange(50.0),weight_dists,cmap='gray')
plt.xlim([0,1])
plt.ylim([0,49])
plt.xlabel('$\mu$')
plt.yticks([])
plt.savefig("exc2c.pdf")
plt.show()
