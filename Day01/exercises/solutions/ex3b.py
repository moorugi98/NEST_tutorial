import nest
import pylab

taum = 10.
Theta = 15.
R = 0.04
tref = 2.
Irh = Theta/R
Irange = pylab.arange(50.0,1000.0,50.0)
simtime = 10.  #in seconds

n = nest.Create('iaf_psc_exp', params={'C_m': 250.0, 'tau_m':10.0, 'V_th':-55.0})
dc = nest.Create('dc_generator')
nest.Connect(dc, n)
sd = nest.Create('spike_detector')
nest.Connect(n,sd)
firing_rates = []
for I in Irange:
    nest.SetStatus(dc,{'amplitude':I})
    nest.Simulate(simtime*1000)   #in ms
    dictsd = nest.GetStatus(sd)[0]
    firing_rates.append((dictsd['events']['times']).size/simtime)
    nest.ResetNetwork()

pylab.figure(1)
pylab.clf()
pylab.plot(Irange, 1000/(taum*pylab.log(Irange/(Irange - Irh)) + tref), 'b-',label='Theoretical firing rate')
#1000 scales up from (ms)^-1 to (s)^-1
pylab.plot(Irange, firing_rates, 'ro',label='Measured firing rate')
pylab.legend(loc='best') 
pylab.show()


# SOLUTION IS THE PLOT
# THEORETICAL VALUE IS DETERMINED BY:
#  firing_rate = 1000/(taum*log(I / (I - Irh)) + tref
