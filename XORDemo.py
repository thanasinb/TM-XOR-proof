#!/usr/bin/python
# import cython
import numpy as np
import pyximport; pyximport.install(setup_args={"include_dirs": np.get_include()}, reload_support=True)

import XOR

X = np.random.randint(2, size=(10000, 2), dtype=np.int32)
Y = np.ones([10000]).astype(dtype=np.int32)

for i in range(10000):
    if X[i, 0] == X[i, 1]:
        Y[i] = 0

# Parameters for the Tsetlin Machine
T = 1
s = 3.9
number_of_clauses = 2
states = 100 
Th = 1
# position_m_array = 0

#########################
# memristor_array new!!!#
#########################

shape = (2, 2, 2)
val = (0.5, 0.505)
cal = 200

memristor_obj = XOR.TsetlinMachine(0, 0, 0, 0, 0, 0, val, shape, cal)
memristor_state = np.array(memristor_obj.get_memristor_state())
# remove decimal output tm_state
tm_state = np.array(memristor_obj.get_tm_state())
ta_state = np.array(memristor_obj.get_ta_state())

# Show List
# print("m_array", np.array(xyz_array).tolist())
print(f"Memristor_state:\n {memristor_state} \n")
print(f"TM_state:\n {tm_state} \n")
print(f"TA_state:\n {ta_state} \n")
print("################ end ##################")
##################################################

# Parameters of the pattern recognition problem
number_of_features = 2

# Training configuration
epochs = 200

# Loading of training and test data
NoOfTrainingSamples = len(X)*80//100
NoOfTestingSamples = len(X) - NoOfTrainingSamples


X_training = X[0:NoOfTrainingSamples, :]  # Input features
y_training = Y[0:NoOfTrainingSamples]  # Target value

X_test = X[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples, :]  # Input features
y_test = Y[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples]  # Target value

# This is a multiclass variant of the Tsetlin Machine, capable of distinguishing between multiple classes
tsetlin_machine = XOR.TsetlinMachine(number_of_clauses, number_of_features, states, s, T, Th, val, shape, cal)

# Training of the Tsetlin Machine in batch mode. The Tsetlin Machine can also be trained online
tsetlin_machine.fit(X_training, y_training, y_training.shape[0], epochs=epochs)

# Some performance statistics

print("Accuracy on test data (no noise):", tsetlin_machine.evaluate(X_test, y_test, y_test.shape[0]))

for clause in range(number_of_clauses):
    print('Clause', clause+1),
    for feature in range(number_of_features):
        for tatype in range(2):
            State = tsetlin_machine.get_state(clause, feature, tatype)
            if State >= 101:
                Decision = 'In'
            else:
                Decision = 'Ex'
            print('feature %d TA %d State %d' % (feature, tatype+1, State)),
    print('/n')
