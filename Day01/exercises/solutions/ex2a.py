import nest
from nest import voltage_trace as vt
import numpy as np

sg = nest.Create("spike_generator", 1, {"spike_times": [200.]})

n_exp = nest.Create("iaf_psc_exp", 1, {"tau_syn_ex": 5.})
n_alpha = nest.Create("iaf_psc_alpha")

mm = nest.Create("multimeter", 1, {"record_from": ["V_m"]})

nest.Connect(mm, n_exp + n_alpha)
nest.Connect(sg, n_alpha)
nest.Connect(sg, n_exp, syn_spec={"weight": 1.3})

nest.Simulate(400)

events = nest.GetStatus(mm, 'events')[0]

senders = events["senders"]
Vm = events["V_m"]
Vm_exp = Vm[np.where(senders == n_exp)]
Vm_alpha = Vm[np.where(senders == n_alpha)]

print max(Vm_exp), max(Vm_alpha)
print np.argmax(Vm_exp), np.argmax(Vm_alpha)

vt.from_device(mm)
vt.show()



# SOLUTION tau_syn = 5. and weight = 1.3, easier to get time first, because time changes the amplitudes


