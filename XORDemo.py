#!/usr/bin/python
# import cython
import numpy as np
import pyximport; pyximport.install(setup_args={
                              "include_dirs":np.get_include()},
                            reload_support=True)

import XOR

X = np.random.randint(2, size=(10000,2), dtype=np.int32)
Y = np.ones([10000]).astype(dtype=np.int32)

for i in range(10000):
    if X[i,0] == X[i,1]:
        Y[i] = 0
# Parameters for the Tsetlin Machine
T = 1
s = 3.9
number_of_clauses = 2
states = 100 
Th = 1

init_memristor_state = 0.5
alpha_off = 1.0
alpha_on = 3.0
v_off = 0.5
v_on = -0.53
r_off = 2.5 * (10 ** 3)
r_on = 100.0
k_off = 4.03 * (10 ** -8)
k_on = -80.0
d = (10 * 10 ** -9)
voltage = 1.2
dt_off = 177 * (10 ** -3)
dt_on = 62 * (10 ** -12)

# Parameters of the pattern recognition problem
number_of_features = 2

# Training configuration
epochs = 200

# Loading of training and test data
NoOfTrainingSamples = len(X)*80//100
NoOfTestingSamples = len(X) - NoOfTrainingSamples


X_training = X[0:NoOfTrainingSamples,:] # Input features
y_training = Y[0:NoOfTrainingSamples] # Target value

X_test = X[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples,:] # Input features
y_test = Y[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples] # Target value

# This is a multiclass variant of the Tsetlin Machine, capable of distinguishing between multiple classes
tsetlin_machine = XOR.TsetlinMachine(number_of_clauses, number_of_features, states, s, T, Th,
                                     init_memristor_state, alpha_off, alpha_on, v_off, v_on, r_off, r_on, k_off, k_on, d,
                                     voltage, dt_off, dt_on)
# tsetlin_machine.print_ta_states()
tsetlin_machine.print_memristor_states()

# Training of the Tsetlin Machine in batch mode. The Tsetlin Machine can also be trained online
tsetlin_machine.fit(X_training, y_training, y_training.shape[0], epochs=epochs)
tsetlin_machine.print_memristor_states()

# Some performacne statistics

print ("Accuracy on test data (no noise):", tsetlin_machine.evaluate(X_test, y_test, y_test.shape[0]))

for clause in range(number_of_clauses):
    print('Clause', clause+1),
    for feature in range(number_of_features):
        for tatype in range(2):
            State = tsetlin_machine.get_state(clause,feature,tatype)
            if State >= 101:
                Decision = 'In'
            else:
                Decision = 'Ex'
            print('feature %d TA %d State %d' % (feature, tatype+1, State)),
    print('/n')
