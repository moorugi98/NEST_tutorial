
### This is the solution for 3c, should be re-named: Jyotika

import nest
import pylab

taum = 10.
Theta = 15.
R = 0.04
tref = 2.
I = 374.
taus = 2.
ratesrange = pylab.arange(0.,1100.,50.)
J = 5.
simtime = 10.  #in seconds

n1 = nest.Create('iaf_psc_exp', params={'C_m': 250.0, 'tau_m':10.0, 'V_th':-55.0, 'tau_syn_ex': taus, 'tau_syn_in':taus})
dc = nest.Create('dc_generator', params={'amplitude': I})
pg_ex1 = nest.Create('poisson_generator')
pg_in1 = nest.Create('poisson_generator')
sd1 = nest.Create('spike_detector')

n2 = nest.Create('iaf_psc_exp_ps', params={'C_m': 250.0, 'tau_m':10.0, 'V_th':-55.0, 'tau_syn_ex': taus, 'tau_syn_in': taus})
pg_ex2 = nest.Create('poisson_generator_ps')
pg_in2 = nest.Create('poisson_generator_ps')
sd2 = nest.Create('spike_detector')

nest.DivergentConnect(dc, n1 + n2)
nest.Connect(pg_ex1, n1, J, 1.0)
nest.Connect(pg_in1, n1, -J, 1.0)
nest.Connect(pg_ex2, n2, J, 1.0)
nest.Connect(pg_in2, n2, -J, 1.0)
nest.Connect(n1,sd1)
nest.Connect(n2,sd2)



firing_rates1 = []
firing_rates2 = []
for r in ratesrange:
    nest.SetStatus(pg_ex1,{'rate':r})
    nest.SetStatus(pg_in1,{'rate':r})
    nest.SetStatus(pg_ex2,{'rate':r})
    nest.SetStatus(pg_in2,{'rate':r})
    nest.Simulate(simtime*1000)   #in ms
    dictsd = nest.GetStatus(sd1)[0]
    firing_rates1.append((dictsd['events']['times']).size/simtime)
    dictsd = nest.GetStatus(sd2)[0]
    firing_rates2.append((dictsd['events']['times']).size/simtime)
    nest.ResetNetwork()
    
pylab.figure(1)
pylab.clf()
pylab.plot(ratesrange*2*J**2*taus/1000, firing_rates1, '.')
pylab.plot(ratesrange*2*J**2*taus/1000, firing_rates2, 'x')
#1000 to convert rates into (ms)^-1
pylab.show()
