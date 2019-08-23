import nest
import pylab

taum = 10.
Theta = 15.
R = 0.04
tref = 2.
I = 374.
taus = 2.
ratesrange = pylab.arange(0.,1100.,10.)
J = 5.
simtime = 10.  #in seconds

def run(rate, J):
    nest.ResetKernel()
    n = nest.Create('iaf_psc_exp', params={'C_m': 250.0, 'tau_m':10.0, 'V_th':-55.0, 'tau_syn_ex': taus})
    dc = nest.Create('dc_generator', params={'amplitude': I})
    pg_ex = nest.Create('poisson_generator', 1, {"rate": rate})
    pg_in = nest.Create('poisson_generator', 1, {"rate": rate})
    sd = nest.Create('spike_detector')
    nest.Connect(dc, n)
    #nest.Connect(pg_ex, n, syn_spec={"weight": J, "delay": 1.0})
    nest.Connect(pg_ex, n, conn_spec={'rule':'all_to_all'}, syn_spec={"weight": J, "delay": 1.0})
    nest.Connect(pg_in, n, conn_spec={'rule':'all_to_all'}, syn_spec={"weight": -J, "delay": 1.0})
    nest.Connect(n,sd)
    nest.Simulate(simtime*1000)   #in ms
    dictsd = nest.GetStatus(sd)[0]
    firing_rates.append((dictsd['events']['times']).size/simtime)


firing_rates = []
for r in ratesrange:
    run(r, J)

pylab.figure(1)
pylab.clf()
pylab.plot(ratesrange*2*J**2*taus/1000, firing_rates, 'bo-')
#pylab.plot(ratesrange,firing_rates, "bo-",label='Measured firing rate')
pylab.xlabel("Input variance")
pylab.ylabel("Measured Neuron firing rate")
pylab.legend()
#1000 to convert rates into (ms)^-1
pylab.show()


# SOLUTION: firing rate is increasing with the variance of the input although the mean input is constant.
