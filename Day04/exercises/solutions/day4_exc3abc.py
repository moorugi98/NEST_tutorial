import nest
import numpy as np
import matplotlib.pyplot as plt # needed for plotting
import matplotlib.cm as cm

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

n_stims = range(5,55,5)
mean_eq_weights = []
hist_stim_wts =[]
hist_non_stim_wts =[]
hist_all_wts=[]
all_wts=[]
for n_stim in n_stims:

    nest.ResetKernel()

    neuron = nest.Create('iaf_psc_alpha',1,{'tau_minus': 20.0})

    # poisson generator with parrot neuron for synch inputs
    stim_rate = 2.0
    pg_sync = nest.Create('poisson_generator',1,{'rate':stim_rate,'start':100000.0})
    par_sync = nest.Create('parrot_neuron',1)
    # Connect the pg to parrot neuron
    nest.Connect(pg_sync,par_sync)	

#    np.random.seed(np.random.randint(1,2338))
#    stim_times = np.sort(np.random.randint(100000,300000,int(stim_rate*200))*0.1)
#    sg_stim = nest.Create('spike_generator',1,{'spike_times': stim_times})

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

    #nest.Connect(sg_stim,inputs[:n_stim],syn_spec={'model':'static_synapse','weight':1.0,'delay':1.0}) # connect stim to first n_stim inputs
    nest.Connect(par_sync,inputs[:n_stim],syn_spec={'model':'static_synapse','weight':1.0,'delay':1.0})
    nest.Connect(pg_exc_stim_0,inputs[:n_stim],syn_spec={'model':'static_synapse','weight':1.0,'delay':1.0}) # before stim
    nest.Connect(pg_exc_stim_1,inputs[:n_stim],syn_spec={'model':'static_synapse','weight':1.0,'delay':1.0}) # during stim
    nest.Connect(pg_exc,inputs[n_stim:],syn_spec={'model':'static_synapse','weight':1.0,'delay':1.0}) # asynch spiking of no stim inputs
    nest.Connect(inputs,neuron,syn_spec={'model':'stdp_synapse','weight':w_exc,'delay':1.0})
    nest.Connect(pg_inh,neuron,syn_spec={'model':'static_synapse','weight':w_inh,'delay':1.0})
    nest.Connect(pg_ext,neuron,syn_spec={'model':'static_synapse','weight':w_exc,'delay':1.0})
    nest.Connect(neuron,sd_post)

    nest.Simulate(200000.0)

    # simulate 100 s, determine mean weights
    stim_connections = nest.GetConnections(inputs[:n_stim])
    no_stim_connections = nest.GetConnections(inputs[n_stim:])
    stim_weights = np.array(nest.GetStatus(stim_connections,'weight'))
    no_stim_weights = np.array(nest.GetStatus(no_stim_connections,'weight'))
    sim_time = 100000.0
    rec_step = 1000.0 # record weights in steps of 1 s
    	
    for t in np.arange(rec_step,sim_time+rec_step,rec_step):
        nest.Simulate(rec_step)
        stim_connections = nest.GetConnections(inputs[:n_stim])
        no_stim_connections = nest.GetConnections(inputs[n_stim:])
    all_wtscon=nest.GetConnections(inputs)
    all_wts=np.append(all_wts,nest.GetStatus(all_wtscon,'weight'))
    stim_weights = np.append(stim_weights,nest.GetStatus(stim_connections,'weight'))
    no_stim_weights = np.append(no_stim_weights,nest.GetStatus(no_stim_connections,'weight'))
		
    mean_eq_weights.append([np.mean(stim_weights), np.mean(no_stim_weights)])
    a1,b1 = np.histogram(stim_weights/(2.*w_exc),bins=10)
    a2,b2 = np.histogram(no_stim_weights/(2.*w_exc),bins=10)
    a3,b3 = np.histogram(all_wts/(2*w_exc),bins=10)
    hist_stim_wts.append(a1)
    hist_non_stim_wts.append(a2)
    hist_all_wts.append(a3)
mean_eq_weights = np.array(mean_eq_weights)
print(mean_eq_weights)

plt.figure(2)
a1,b1 = np.histogram(stim_weights/(2.*w_exc),bins=10)
a2,b2 = np.histogram(no_stim_weights/(2.*w_exc),bins=10)
plt.step(b1[:-1],a1,'b-',label="synchronous")
plt.step(b2[:-1],a2,'r-',label="asyn")
plt.xlabel("Normalized weights")
plt.ylabel("#")
plt.title("Histogram of sync and aync weights")
plt.legend()


# plot mean eq. weights
plt.figure(1)
plt.plot(n_stims,mean_eq_weights[:,1]/(2.0*w_exc),'r.-',label='async') # max. weight is 2*w_exc
plt.plot(n_stims,mean_eq_weights[:,0]/(2.0*w_exc),'b.-',label='sync')
plt.xlim([0,50])
plt.ylim([0,1])
plt.xlabel('n_stim')
plt.ylabel('mean eq. weight')
plt.savefig("exc3c.pdf")
plt.legend()

'''
plt.figure()
plt.pcolor(hist_stim_wts)
plt.colorbar()
plt.title("Stim")
plt.figure()
plt.pcolor(hist_non_stim_wts)
plt.colorbar()
plt.title("Non stim")
plt.figure()
plt.pcolor(hist_all_wts)
plt.colorbar()
plt.title("All")
'''
plt.show()
