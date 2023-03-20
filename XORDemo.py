#!/usr/bin/python
# import cython
import sys
from ctypes import cdll, c_int, c_bool, c_double, byref, c_ubyte
from datetime import time

import numpy as np
import pyximport;

pyximport.install(setup_args={
    "include_dirs": np.get_include()},
    reload_support=True)

import XOR

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

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
hdwf = c_int()
channel = c_int(0)
Vwrite = 0.3
Vread = 0.1
nSamples = 3000
value = True
measure = True
sleep_in = 0.1
sleep_out = 2
Rs = 5000
AnalogOutNodeCarrier = c_int(0)
DwfStateDone = c_ubyte(2)

memristor_states = np.ones([2])


def write_memristor(memristor_no, state):
    while measure:
        dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))
        sts = c_int()
        while True:
            dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value:
                break
            time.sleep(sleep_in)

        rg = (c_double * nSamples)()
        dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rg, len(rg))  # get channel 2 data

        Va = sum(rg) / len(rg)
        R_write = ((Vwrite * Rs) / Va) - Rs

    if state >= 101:
        memristor_states[memristor_no] = 110  # Include Ron 10k
        if R_write < 100000:
            print('Ron LOW: ' + R_write)
    else:
        memristor_states[memristor_no] = 90  # Exclude Roff High
        print('Roff HIGH: ' + R_write)
    return


def read_memristor(memristor_no):
    state = memristor_states[memristor_no]
    while value:
        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(Vread))
        dwf.FDwfAnalogOutConfigure(hdwf, channel, c_bool(True))
        time.sleep(sleep_out)

        dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(1))
        sts = c_int()
        while True:
            dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value:
                break
            time.sleep(sleep_in)

        dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(0))
        dwf.FDwfAnalogOutConfigure(hdwf, channel, c_bool(True))
        time.sleep(sleep_out)

        rg = (c_double * nSamples)()
        dwf.FDwfAnalogInStatusData(hdwf, c_int(1), rg, len(rg))  # get channel 1 data

        Va_read = sum(rg) / len(rg)
        print("Va_read: " + str(Va_read) + "V")

        R_read = ((Vread * Rs) / Va_read) - Rs
        print("R_read: " + str(R_read))
    if R_read > 100000:
        state = 90
    else:
        state = 110
    return state


# Parameters of the pattern recognition problem
number_of_features = 2

# Training configuration
epochs = 200

# Loading of training and test data
NoOfTrainingSamples = len(X) * 80 // 100
NoOfTestingSamples = len(X) - NoOfTrainingSamples

X_training = X[0:NoOfTrainingSamples, :]  # Input features
y_training = Y[0:NoOfTrainingSamples]  # Target value

X_test = X[NoOfTrainingSamples:NoOfTrainingSamples + NoOfTestingSamples, :]  # Input features
y_test = Y[NoOfTrainingSamples:NoOfTrainingSamples + NoOfTestingSamples]  # Target value

# This is a multiclass variant of the Tsetlin Machine, capable of distinguishing between multiple classes
tsetlin_machine = XOR.TsetlinMachine(number_of_clauses, number_of_features, states, s, T, Th)

# Training of the Tsetlin Machine in batch mode. The Tsetlin Machine can also be trained online
tsetlin_machine.fit(X_training, y_training, y_training.shape[0], epochs=epochs)

clause = 0
feature = 0
tatype = 0
memristor_no = 0
State = tsetlin_machine.get_state(clause, feature, tatype)
write_memristor(memristor_no, State)
print('Clause', clause + 1),
print('feature %d TA %d State %d' % (feature, tatype + 1, State))

clause = 0
feature = 0
tatype = 1
memristor_no = 1
State = tsetlin_machine.get_state(clause, feature, tatype)
write_memristor(memristor_no, State)
print('Clause', clause + 1),
print('feature %d TA %d State %d' % (feature, tatype + 1, State))

clause = 0
feature = 0
tatype = 0
memristor_no = 0
tsetlin_machine.set_state(clause, feature, tatype, read_memristor(memristor_no))
print('Clause', clause + 1),
print('feature %d TA %d State %d' % (feature, tatype + 1, tsetlin_machine.get_state(clause, feature, tatype)))

clause = 0
feature = 0
tatype = 1
memristor_no = 1
tsetlin_machine.set_state(clause, feature, tatype, read_memristor(memristor_no))
print('Clause', clause + 1),
print('feature %d TA %d State %d' % (feature, tatype + 1, tsetlin_machine.get_state(clause, feature, tatype)))

# Some performacne statistics

print("Accuracy on test data (no noise):", tsetlin_machine.evaluate(X_test, y_test, y_test.shape[0]))

for clause in range(number_of_clauses):
    print('Clause', clause + 1),
    for feature in range(number_of_features):
        for tatype in range(2):
            State = tsetlin_machine.get_state(clause, feature, tatype)
            if State >= 101:
                Decision = 'In'
            else:
                Decision = 'Ex'
            print('feature %d TA %d State %d' % (feature, tatype + 1, State)),
    print('/n')
