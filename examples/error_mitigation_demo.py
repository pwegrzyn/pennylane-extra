"""
    Adapted from https://pennylane.ai/qml/demos/tutorial_qubit_rotation.html
"""

import qiskit
import pennylane as qml
import pennylane_extra
from pennylane import numpy as np

# Init account to connect to IBMQ
qiskit.IBMQ.load_account()

# Build noise model from backend properties
provider = qiskit.IBMQ.get_provider(group='open')
ibmq_backend = provider.get_backend('ibmq_burlington')
device_properties = ibmq_backend.properties()
noise_model = qiskit.providers.aer.noise.NoiseModel.from_backend(device_properties)

# Get coupling map from backend
coupling_map = ibmq_backend.configuration().coupling_map

# Get basis gates from noise model
basis_gates = noise_model.basis_gates

# Provision the the device
dev1 = qml.device('qiskit.aer', wires=2, noise_model=noise_model, basis_gates=basis_gates, coupling_map=coupling_map, backend='qasm_simulator', shots=10000)

# @qml.qnode(dev1)
# def circuit(params):
#     qml.RX(params[0], wires=0)
#     qml.RY(params[1], wires=0)
#     return qml.expval(qml.PauliZ(0))

# def cost(var):
#     return circuit(var)

# init_params = np.array([0.011, 0.012])

# def train():
#     # initialise the optimizer
#     opt = qml.GradientDescentOptimizer(stepsize=0.4)

#     # set the number of steps
#     steps = 100
#     # set the initial parameter values
#     params = init_params

#     for i in range(steps):
#         # update the circuit parameters
#         params = opt.step(cost, params)

#         if (i + 1) % 5 == 0:
#             print("Cost after step {:5d}: {: .7f}".format(i + 1, cost(params)))

#     print("Optimized rotation angles: {}".format(params))

# print("Running training WITHOUT measurement error mitigation...")
# train()

# # now let's test the model with measurement error mitigation
# pennylane_extra.enable_qiskit_measurement_error_mitigation_on_qnode(circuit)

# print("Running training WITH measurement error mitigation...")
# train()

@qml.qnode(dev1)
def circuit():
    qml.PauliX(0)
    return qml.probs(wires=[0, 1])

print(circuit())

with pennylane_extra.qiskit_measurement_error_mitigation():
    print(circuit())