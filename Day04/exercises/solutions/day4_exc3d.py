import nest
import numpy as np
import matplotlib.pyplot as plt # needed for plotting

np.random.seed(92)

C  = 125
CE = int(0.8*C)
CI = int(0.2*C)

rate   = 10.0
nu_ext =  5.0

g     = -5.0
w_exc = 70.0
w_inh = g*w_exc

alpha = 1.1 # results in firing rate of 8.5 to 9 Hz

#mu = 0.0 # additive rule
mu = 1.0 # multiplicative rule

stim_rate = 2.0
#stim_times = np.sort(np.random.randint(1000000,3000000,int(stim_rate*200))*0.1)

n_stims = range(5,55,5)
mean_eq_weights = []
for n_stim in n_stims:

    nest.ResetKernel()

    neuron = nest.Create('iaf_psc_alpha',1,{'tau_minus': 20.0})

    # poisson generator to parrot neuron for synch inputs
    pg_sync = nest.Create('poisson_generator',1,{'rate':stim_rate,'start':100000.0})
    par_sync = nest.Create('parrot_neuron',1)
    # Connect the pg to parrot neuron
    nest.Connect(pg_sync,par_sync)	


    # decreased asynch spiking of stim inputs
    pg_exc_stim_0 = nest.Create('poisson_generator',1,{'rate': rate, 'stop': 100000.0}) # before stim
    pg_exc_stim_1 = nest.Create('poisson_generator',1,{'rate': rate-stim_rate, 'start': 100000.0}) # during stim
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

    nest.Connect(par_sync,inputs[:n_stim],syn_spec={"weight":1.0,"delay":1.0,"model":'static_synapse'}) # connect stim to first n_stim inputs , all n_stim will have same input, synch
    nest.Connect(pg_exc_stim_0,inputs[:n_stim],syn_spec={"weight":1.0,"delay":1.0,"model":'static_synapse'}) # before stim, 
    nest.Connect(pg_exc_stim_1,inputs[:n_stim],syn_spec={"weight":1.0,"delay":1.0,"model":'static_synapse'}) # during stim, 
    nest.Connect(pg_exc,inputs[n_stim:],syn_spec={"weight":1.0,"delay":1.0,"model":'static_synapse'}) # asynch spiking of no stim inputs
    nest.Connect(inputs,neuron,syn_spec={"weight":w_exc,"delay":1.0,"model":'stdp_synapse'})
    nest.Connect(pg_inh,neuron,syn_spec={"weight":w_inh,"delay":1.0,"model":'static_synapse'})
    nest.Connect(pg_ext,neuron,syn_spec={"weight":w_exc,"delay":1.0,"model":'static_synapse'})
#    nest.Connect(pg_exc,sd_post)
    nest.Connect(neuron,sd_post)

    nest.Simulate(100000.0)
    connections = nest.GetConnections(inputs, neuron)
    weights = nest.GetStatus(connections,'weight')
    w_total_eq = np.sum(weights) # target total for homeostasis
    
    # simulate 200 s, determine mean weights
    stim_connections = nest.GetConnections(inputs[:n_stim],neuron)
    no_stim_connections = nest.GetConnections(inputs[n_stim:],neuron)
    stim_weights = np.array(nest.GetStatus(stim_connections,'weight'))
    no_stim_weights = np.array(nest.GetStatus(no_stim_connections,'weight'))
    sim_time = 200000.0
    rec_step =   1000.0 # record weights in steps of 1 s
    for t in np.arange(rec_step,sim_time+rec_step,rec_step):
        nest.Simulate(rec_step)
	# Weights recorded before homeostasis
        stim_connections = nest.GetConnections(inputs[:n_stim],neuron)
        no_stim_connections = nest.GetConnections(inputs[n_stim:],neuron)
        stim_weights = np.append(stim_weights,nest.GetStatus(stim_connections,'weight'))
        no_stim_weights = np.append(no_stim_weights,nest.GetStatus(no_stim_connections,'weight'))
        # dendritic homeostasis
        connections = nest.GetConnections(inputs,neuron)
        weights = np.array(nest.GetStatus(connections,'weight'))
        weights = weights * (w_total_eq / np.sum(weights))
        nest.SetStatus(connections,params='weight',val=weights)

    mean_eq_weights.append([np.mean(stim_weights), np.mean(no_stim_weights)])

mean_eq_weights = np.array(mean_eq_weights)

# plot mean eq. weights
plt.figure(1)
plt.plot(n_stims,mean_eq_weights[:,0]/(2.0*w_exc),'b-',label='Synch weights') # max. weight is 2*w_exc
plt.plot(n_stims,mean_eq_weights[:,1]/(2.0*w_exc),'r-',label='Asynch weights')
plt.xlim([0,50])
plt.ylim([0,1])
plt.xlabel('n_stim')
plt.ylabel('mean eq. weight')
plt.legend()
plt.savefig("exc3d.pdf")
plt.show()
