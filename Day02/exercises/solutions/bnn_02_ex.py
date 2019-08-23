import pylab
import numpy
import nest

###################################################################
## parameters

## simulation parameters
T=1000.                  ## simulation time (ms)
dt=0.1                   ## simulation time resolution (ms)
seed=1                   ## RNG seed

## network parameters
N=12500                  ## number of neurons
epsilon=0.1              ## connectivity
gamma=0.8                ## fraction of excitatory neurons and synapses

## neuron parameters
Vth=-55.                 ## spike threshold
Vrest=-70.               ## resting potential
## (use default parameters for C_m, tau_m, t_ref, ...)

## synapse parameters
JE=0.2                   ## excitatory weight (mV)
g=6                      ## relative inhibitory weigth
d=0.1                    ## spike transmission delay (ms)

## input parameters
Iext=400.                ## DC input (pA)

## data analysis parameters
h=10.                    ## bin width of spike count signal (ms)

###################################################################
## derived parameters

NE=pylab.int0(gamma*N)   ## number of excitatory neurons
NI=N-NE                  ## number of inhibitory neurons
K=pylab.int0(epsilon*N)  ## toal in-degree
KE=pylab.int0(gamma*K)   ## excitatory in-degree
KI=K-KE                  ## inhibitory in-degree
JI=-g*JE                 ## inhibitory synaptic weight

###################################
## network type I
print "\nNetwork type I"

## reset numpy RNG seed
numpy.random.seed(seed)

## reset kernel and set time resolution
nest.ResetKernel()
nest.SetKernelStatus({'resolution':dt})

## set default neuron parameters
nest.SetDefaults('iaf_psc_delta',{'I_e': Iext, 'E_L': Vrest, 'V_th': Vth, 'V_reset': Vrest})

## create neurons
pop=nest.Create('iaf_psc_delta',N)

## set up and connect spike detector
sd=nest.Create('spike_detector')
#nest.ConvergentConnect(pop,sd)
nest.Connect(pop,sd)

## connect network
#nest.RandomConvergentConnect(pop,pop,KE,weight=JE,delay=d)
#nest.RandomConvergentConnect(pop,pop,KI,weight=JI,delay=d)
nest.Connect(pop, pop, {"rule": "fixed_indegree", "indegree": KE}, {"weight": JE, "delay": d})
nest.Connect(pop, pop, {"rule": "fixed_indegree", "indegree": KI}, {"weight": JI, "delay": d})

## random initial conditions
nest.SetStatus(pop,'V_m',Vrest+(Vth-Vrest)*numpy.random.rand(N))

nest.Simulate(T)

## read spike data
sd_dict = nest.GetStatus(sd,keys='events')[0]
spike_senders_I= sd_dict['senders']
spike_times_I= sd_dict['times']

###################################
## network type II
print "\nNetwork type II"

## reset numpy RNG seed
numpy.random.seed(seed)

## reset kernel and set time resolution
nest.ResetKernel()
nest.SetKernelStatus({'resolution':dt})

## set default neuron parameters
nest.SetDefaults('iaf_psc_delta',{'I_e': Iext, 'E_L': Vrest, 'V_th': Vth, 'V_reset': Vrest})

## create neuron populations
popE=nest.Create('iaf_psc_delta',NE) ## excitatory population
popI=nest.Create('iaf_psc_delta',NI) ## inhibitory population
pop=popE+popI ## full population

## set up and connect spike detector
sd=nest.Create('spike_detector')
nest.Connect(pop,sd)

## connect network
#nest.RandomConvergentConnect(popE,pop,KE,weight=JE,delay=d)
#nest.RandomConvergentConnect(popI,pop,KI,weight=JI,delay=d)
nest.Connect(popE, pop, {"rule": "fixed_indegree", "indegree": KE}, {"weight": JE, "delay": d})
nest.Connect(popI, pop, {"rule": "fixed_indegree", "indegree": KI}, {"weight": JI, "delay": d})

## random initial conditions
nest.SetStatus(pop,'V_m',Vrest+(Vth-Vrest)*numpy.random.rand(N))

nest.Simulate(T)

## read spike data
sd_dict = nest.GetStatus(sd,keys='events')[0]
spike_senders_II= sd_dict['senders']
spike_times_II= sd_dict['times']

###################################
## data analysis

## firing rates
rate_I=numpy.float(len(spike_times_I))/T*1e3/N
rate_II=numpy.float(len(spike_times_II))/T*1e3/N

## spike count statistics
times=numpy.arange(0,T+h,h)                     ## array of times
n_I=numpy.histogram(spike_times_I,times)[0]     ## pop spike count histogram
n_II=numpy.histogram(spike_times_II,times)[0]   ## pop spike count histogram
F_I=numpy.var(n_I)/numpy.mean(n_I)              ## Fano factor
F_II=numpy.var(n_II)/numpy.mean(n_II)           ## Fano factor

print "Firing rate I = %.1f spikes/s" % (rate_I)
print "Firing rate II = %.1f spikes/s" % (rate_II)
print "Fano factor I = %.1f" % (F_I)
print "Fano factor II = %.1f" % (F_II)

###################################
# plotting
pylab.rcdefaults() 
pylab.rcParams['figure.figsize'] = (8,12)
pylab.rcParams['font.size']= 10
pylab.figure(1)
pylab.clf()

pylab.subplot(411)
pylab.plot(spike_times_I,spike_senders_I,'k.',markersize=1)
pylab.xlim(0,T)
pylab.ylim(pop[0],pop[-1])
pylab.title('Network type I')
pylab.setp(pylab.gca(),xticklabels=[])
pylab.ylabel('neuron id')

pylab.subplot(412)
pylab.bar(times[:-1],n_I,h,color='k')
pylab.setp(pylab.gca(),xticklabels=[])
pylab.xlim(0,T)
pylab.ylim(0,1.2*numpy.max(pylab.concatenate((n_I,n_II))))
pylab.ylabel('spike count')

pylab.subplot(413)
pylab.plot(spike_times_II,spike_senders_II,'k.',markersize=1)
pylab.xlim(0,T)
pylab.ylim(pop[0],pop[-1])
pylab.title('Network type II')
pylab.setp(pylab.gca(),xticklabels=[])
pylab.ylabel('neuron id')

pylab.subplot(414)
pylab.bar(times[:-1],n_II,h,color='k')
pylab.xlim(0,T)
pylab.ylim(0,1.2*numpy.max(pylab.concatenate((n_I,n_II))))
pylab.ylabel('spike count')
pylab.xlabel('time (ms)')

pylab.savefig('bnn_02_ex2_fig.png',dpi=300)
