import nest
import numpy as np
import matplotlib.pyplot as plt # needed for plotting

# params
C  = 125
CE = int(0.8 * C)
CI = int(0.2 * C)
rate   = 10.0
nu_ext =  5.0

g     = -5.0
w_exc = 70.0
w_inh = g * w_exc
alpha = 1.1 # OK WHY

# check for addtive and multiplicative rules
mus = [0.0, 1.0] #[additive, multiplicative]
for mu in mus:

    nest.ResetKernel()

    # create ndoes
    neuron = nest.Create("iaf_psc_alpha", 1, {"tau_minus": 20.0})

    pg_exc = nest.Create("poisson_generator", 1, {"rate": rate})
    inputs = nest.Create("parrot_neuron",CE)

    pg_inh = nest.Create("poisson_generator", 1, {"rate": CI * rate})
    pg_ext = nest.Create("poisson_generator", 1, {"rate": CE * nu_ext})

    nest.SetDefaults("stdp_synapse",{"tau_plus": 20.0,
                                     "mu_plus":  mu, # weight dep potent.
                                     "mu_minus": mu, # weight dep. depr.
                                     "alpha":    alpha,
                                     "lambda":   0.1,
                                     "Wmax":     2.0 * w_exc})

    nest.Connect(pg_exc, inputs, "all_to_all", {"weight":1.0, "delay":1.0,
                                                "model":"static_synapse"})
    nest.Connect(pg_inh, neuron, "all_to_all", {"weight":w_inh, "delay":1.0,
                                                "model":"static_synapse"})
    nest.Connect(pg_ext, neuron, "all_to_all", {"weight":w_exc, "delay":1.0,
                                                "model":"static_synapse"})
    nest.Connect(inputs, neuron, "all_to_all", {"weight":w_exc, "delay":1.0,
                                                "model":"stdp_synapse"}) # STDP

    nest.Simulate(1)
    conn = nest.GetConnections(inputs)
    weights = nest.GetStatus(conn,"weight")
print(weights)

