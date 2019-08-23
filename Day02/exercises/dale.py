import nest
import numpy as np
from params import *

gamma = 0.8
epsilon = 0.1
K = epsilon*N

epop = nest.Create(model, int(gamma*N), params={"E_L":E_L, "V_th":V_th, "V_reset":V_reset, "C_m":C_m,
     "tau_m":tau_m, "I_e":I_e})
ipop = nest.Create(model, int((1-gamma)*N), params={"E_L":E_L, "V_th":V_th, "V_reset":V_reset, "C_m":C_m,
     "tau_m":tau_m, "I_e":I_e})

nest.SetStatus(epop, [{"V_m":np.random.uniform(E_L,V_th)} for neuron in epop])
nest.SetStatus(ipop, [{"V_m":np.random.uniform(E_L,V_th)} for neuron in ipop])

nest.Connect(epop, ipop, {"rule":"fixed_indegree", "indegree":int(gamma*K)}, {"weight":J_E, "delay":d})
nest.Connect(epop, epop, {"rule":"fixed_indegree", "indegree":int(gamma*K)}, {"weight":J_E, "delay":d})
nest.Connect(ipop, ipop, {"rule":"fixed_indegree", "indegree":int((1-gamma)*K)}, {"weight":-1*g*J_E, "delay":d})
nest.Connect(ipop, epop, {"rule":"fixed_indegree", "indegree":int((1-gamma)*K)}, {"weight":-1*g*J_E, "delay":d})#



spike_device = nest.Create("spike_detector", params={"withtime":True, "to_file":False, "label":"dale"})
nest.Connect(epop,spike_device)
nest.Connect(ipop,spike_device)

