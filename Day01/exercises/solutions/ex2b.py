import nest
from nest import voltage_trace as vt
import numpy as np

nest.ResetKernel()
sg = nest.Create("spike_generator", 1, {"spike_times": [200.]})

#n_exp = nest.Create("iaf_psc_exp", 1, {"I_e": 188.}) # Potential before spike ~ -62.48
#n_cond = nest.Create("iaf_cond_exp", 1, {"I_e": 125.}) # Potential before spike ~ -62.5

#n_exp = nest.Create("iaf_psc_exp", 1, {"I_e": 0.}) # Potential before spike ~ -70
#n_cond = nest.Create("iaf_cond_exp", 1, {"I_e": 0.}) # Potential before spike ~ -70

n_exp = nest.Create("iaf_psc_exp", 1, {"I_e": -188.}) # Potential before spike ~ -77
n_cond = nest.Create("iaf_cond_exp", 1, {"I_e": -125.}) # Potential before spike ~ -77


#n_exp = nest.Create("iaf_psc_exp", 1, {"I_e": 300.})
#n_cond = nest.Create("iaf_cond_exp", 1, {"I_e": 200.})

mm = nest.Create("multimeter", 1, {"record_from": ["V_m"], "start": 100.})

nest.Connect(mm, n_exp + n_cond)
nest.Connect(sg, n_cond)
#nest.Connect(sg, n_exp, syn_spec={"weight": 1.0})
nest.Connect(sg, n_exp, syn_spec={"weight": 1.0})

nest.Simulate(400)

events = nest.GetStatus(mm, 'events')[0]

senders = events["senders"]
times = events["times"]
Vm = events["V_m"]
Vm_exp = Vm[np.where(senders == n_exp)]
Vm_cond = Vm[np.where(senders == n_cond)]

Vm_exp_b4 = Vm[np.logical_and(times < 199,senders==n_exp)]
Vm_cond_b4 = Vm[np.logical_and(times < 199,senders==n_cond)]
print "Amplitudes of psc_exp and cond_exp before spike"
print np.mean(Vm_exp_b4) , np.mean(Vm_cond_b4)
print "Amplitudes of psc_exp and cond_exp after spike"
print max(Vm_exp), max(Vm_cond)
print "PSP sizes for psc_exp and cond_exp after spike"
print np.mean(Vm_exp_b4)-max(Vm_exp) , np.mean(Vm_cond_b4)-max(Vm_cond)
print np.argmax(Vm_exp), np.argmax(Vm_cond)

 
vt.from_device(mm)
vt.show()

# V_m baseline for I_e = 300 / 200:         -58.
# V_m baseline for I_e = -300 / -200:       -82.

# SOLUTION
# With +ve background
#Amplitudes of psc_exp and cond_exp before spike
#-62.4800000189 -62.5000288791
#Amplitudes of psc_exp and cond_exp after spike
#-62.4746501618 -62.4529781256
#PSP sizes for psc_exp and cond_exp after spike
#-0.00534985715843 -0.0470507534623


# Without +ve background
#Amplitudes of psc_exp and cond_exp before spike
#-70.0 -70.0
#Amplitudes of psc_exp and cond_exp after spike
#-69.9946501524 -69.9473068168
#PSP sizes for psc_exp and cond_exp after spike
#-0.005349847628 -0.0526931832157

# With -ve background
#Amplitudes of psc_exp and cond_exp before spike
#-77.5199668772 -77.498574304
#Amplitudes of psc_exp and cond_exp after spike
#-77.514650143 -77.4416355079
#PSP sizes for psc_exp and cond_exp after spike
#-0.00531673421727 -0.0569387960088


# with positive background:     psc: 0.005 cond: 0.04
# without positive background:  psc: 0.005 cond: 0.05
# with negative background:     psc: 0.005 cond: 0.06

