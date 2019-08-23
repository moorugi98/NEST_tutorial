import nest
import pylab

#I = 375.0  #doesn't fire
I = 375.001  #fires
n = nest.Create('iaf_psc_exp', params={'C_m': 250.0, 'tau_m':10.0, 'V_th':-55.0})
#or a Create followed by a SetStatus

dc = nest.Create('dc_generator', params={'amplitude': I})
nest.Connect(dc, n)
#or set the I_e parameter in the neuron

sd = nest.Create('spike_detector')
nest.Connect(n,sd)

nest.Simulate(10000)
dictsd = nest.GetStatus(sd)[0]
ns = dictsd['events']['senders']
ts = dictsd['events']['times']

pylab.figure(1)
pylab.clf()
pylab.plot(ts, ns, '.') 
pylab.show()


#SOLUTION: I_rh = 375.
