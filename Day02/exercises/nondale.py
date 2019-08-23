from params import *
import nest
import numpy as np

pop = nest.Create(model, N, params={"E_L":E_L, "V_th":V_th, "V_reset":V_reset, "C_m":C_m,
     "tau_m":tau_m, "I_e":I_e})

gamma = 0.8
epsilon = 0.1
K = epsilon * N

vms = [{"V_m":np.random.uniform(E_L,V_th)} for neuron in pop]
nest.SetStatus(pop, vms)

nest.Connect(pop, pop, {"rule":"fixed_indegree", "indegree":int(gamma*K)}, {"weight":J_E, "delay":d})
nest.Connect(pop, pop, {"rule":"fixed_indegree", "indegree":int((1-gamma)*K)}, {"weight":-1*g*J_E, "delay":d})

spike_device = nest.Create("spike_detector", params={"withtime":True, "to_file":False, "label":"nondale"})
print(spike_device)
nest.Connect(pop,spike_device)

# nest.SetKernelStatus({"data_path": "datas/", "overwrite_files": True})
# nest.Simulate(T)