# Copyright (c) 2019 Ole-Christoffer Granmo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This code implements a multiclass version of the Tsetlin Machine from paper arXiv:1804.01508
# https://arxiv.org/abs/1804.01508

#cython: boundscheck=False, cdivision=True, initializedcheck=False, nonecheck=False

import numpy as np
cimport numpy as np
import random
from libc.stdlib cimport rand, RAND_MAX
from memristor cimport Memristor
import csv
import os

#############################
### The Tsetlin Machine #####
#############################

cdef class TsetlinMachine:
	cdef int number_of_clauses
	cdef int number_of_features
	
	cdef float s
	cdef int number_of_states
	cdef int threshold
	cdef int Th

	cdef int[:,:,:] ta_state
	cdef int[:] clause_sign
	cdef int[:] clause_output
	cdef int[:] feedback_to_clauses

	cdef Memristor[:,:,:] memristors
	cdef float init_memristor_state
	cdef float alpha_off
	cdef float alpha_on
	cdef float v_off
	cdef float v_on
	cdef float r_off
	cdef float r_on
	cdef float k_off
	cdef float k_on
	cdef float d
	cdef float voltage
	cdef float dt_off
	cdef float dt_on

	mycsv = {}
	csvwriter = {}

	# Initialization of the Tsetlin Machine
	def __init__(self, number_of_clauses, number_of_features, number_of_states, s, threshold, Th,
				 init_memristor_state, alpha_off, alpha_on, v_off, v_on, r_off, r_on, k_off, k_on, d,
				 voltage, dt_off, dt_on):
		cdef int j

		self.number_of_clauses = number_of_clauses
		self.number_of_features = number_of_features
		self.number_of_states = number_of_states
		self.s = s
		self.threshold = threshold
		self.Th = Th
		self.init_memristor_state = init_memristor_state
		self.alpha_off = alpha_off
		self.alpha_on = alpha_on
		self.v_off = v_off
		self.v_on = v_on
		self.r_off = r_off
		self.r_on = r_on
		self.k_off = k_off
		self.k_on = k_on
		self.d = d
		self.voltage = voltage
		self.dt_off = dt_off
		self.dt_on = dt_on

		# The state of each Tsetlin Automaton is stored here. The automata are randomly initialized to either 'number_of_states' or 'number_of_states' + 1.
		self.ta_state = np.random.choice([self.number_of_states, self.number_of_states+1], size=(self.number_of_clauses, self.number_of_features, 2)).astype(dtype=np.int32)

		self.memristors = np.empty((self.number_of_clauses, self.number_of_features, 2), dtype=object)
		for a in range(self.number_of_clauses):
			for b in range(self.number_of_features):
				for c in range(2):
					self.memristors[a, b, c] = Memristor(self.ta_state[a, b, c], init_memristor_state, number_of_states,
														 self.alpha_off, self.alpha_on,
														 self.v_off, self.v_on,
														 self.r_off, self.r_on,
														 self.k_off, self.k_on,
														 self.d, a, b, c)

		# int ta_state, float init_memristor_state, int number_of_states,
		# float alpha_off, float alpha_on, float v_off, float v_on, float r_off, float r_on, float k_off, float k_on, float d

		# Data structure for keeping track of the sign of each clause
		self.clause_sign = np.zeros(self.number_of_clauses, dtype=np.int32)
		
		# Data structures for intermediate calculations (clause output, summation of votes, and feedback to clauses)
		self.clause_output = np.zeros(shape=(self.number_of_clauses), dtype=np.int32)
		self.feedback_to_clauses = np.zeros(shape=(self.number_of_clauses), dtype=np.int32)

		# Set up the Tsetlin Machine structure
		for j in xrange(self.number_of_clauses):
			if j % 2 == 0:
				self.clause_sign[j] = 1
			else:
				self.clause_sign[j] = 1

		self.init_csv()

	def print_ta_states(self):
		"""
        Print the values inside the ta_state ndarray.
        """
		cdef int i, j, k
		for i in range(self.ta_state.shape[0]):
			for j in range(self.ta_state.shape[1]):
				for k in range(self.ta_state.shape[2]):
					print(f"ta_state[{i},{j},{k}] = {self.ta_state[i, j, k]}")
		print(f"\n")

	def print_memristor_states(self):
		"""
        Print the states of the memristor array.
        """
		cdef int i, j, k
		for i in range(self.memristors.shape[0]):
			for j in range(self.memristors.shape[1]):
				for k in range(self.memristors.shape[2]):
					print(f"memristors[{i},{j},{k}].state = {self.memristors[i, j, k].get_mr_state()}, {self.memristors[i, j, k].get_ta_state()}")
		print(f"\n")

	def init_csv(self):
		cdef int i, j, k
		cdef float mr_state, mr_dx, mr_x
		for i in range(self.memristors.shape[0]):
			for j in range(self.memristors.shape[1]):
				for k in range(self.memristors.shape[2]):
					if os.path.exists(f"memristor{i}{j}{k}.csv"):
						os.remove(f"memristor{i}{j}{k}.csv")

					with open(f"memristor{i}{j}{k}.csv", 'w', newline='') as csvfile:
						writer = csv.DictWriter(csvfile, fieldnames=["TA State", "Memristor State", "Distance Shift", "Final Distance"])
						writer.writeheader()
						csvfile.close()

					self.mycsv[i, j, k] = open(f"memristor{i}{j}{k}.csv", 'a', newline='')
					self.csvwriter[i, j, k] = csv.writer(self.mycsv[i, j, k])
					mr_ta_state, mr_state, mr_dx, mr_x = self.memristors[i, j, k].get_mr_xdx()
					self.csvwriter[i, j, k].writerow([mr_ta_state, mr_state, mr_dx, mr_x])

	def append_csv(self):
		cdef int i, j, k, mr_ta_state
		cdef float mr_state, mr_dx, mr_x
		for i in range(self.memristors.shape[0]):
			for j in range(self.memristors.shape[1]):
				for k in range(self.memristors.shape[2]):
					mr_ta_state, mr_state, mr_dx, mr_x = self.memristors[i, j, k].get_mr_xdx()
					self.csvwriter[i, j, k].writerow([mr_ta_state, mr_state, mr_dx, mr_x])

	def close_csv(self):
		cdef int i, j, k, mr_ta_state
		cdef float mr_state, mr_dx, mr_x
		for i in range(self.memristors.shape[0]):
			for j in range(self.memristors.shape[1]):
				for k in range(self.memristors.shape[2]):
					self.mycsv[i, j, k].close()


	# Calculate the output of each clause using the actions of each Tsetline Automaton.
	# Output is stored an internal output array.
	cdef void calculate_clause_output(self, int[:] X):
		cdef int j, k

		for j in xrange(self.number_of_clauses):				
			self.clause_output[j] = 1
			for k in xrange(self.number_of_features):
				action_include = self.action(self.memristors[j,k,0].get_ta_state())
				action_include_negated = self.action(self.memristors[j,k,1].get_ta_state())

				if (action_include == 1 and X[k] == 0) or (action_include_negated == 1 and X[k] == 1):
					self.clause_output[j] = 0
					break

	###########################################
	### Predict Target Output y for Input X ###
	###########################################

	cpdef int predict(self, int[:] X):
		cdef int output_sum
		cdef int j
		
		###############################
		### Calculate Clause Output ###
		###############################

		self.calculate_clause_output(X)

		###########################
		### Sum up Clause Votes ###
		###########################

		output_sum = self.sum_up_clause_votes()

		if output_sum >= self.Th:
			return 1
		else:
			return 0

	# Translates automata state to action 
	cdef int action(self, int state):
		if state <= self.number_of_states:
			return 0
		else:
			return 1

	# Get the state of a specific automaton, indexed by clause, feature, and automaton type (include/include negated).
	def get_state(self, int clause, int feature, int automaton_type):
		return self.memristors[clause,feature,automaton_type].get_ta_state()

	# Sum up the votes for each output decision (y=0 or y = 1)
	cdef int sum_up_clause_votes(self):
		cdef int output_sum
		cdef int j

		output_sum = 0
		for j in xrange(self.number_of_clauses):
			output_sum += self.clause_output[j]*self.clause_sign[j]
		
		if output_sum > self.threshold:
			output_sum = self.threshold
		
		elif output_sum < self.Th:
			output_sum = 0

		return output_sum

	############################################
	### Evaluate the Trained Tsetlin Machine ###
	############################################

	def evaluate(self, int[:,:] X, int[:] y, int number_of_examples):
		cdef int j,l
		cdef int errors
		cdef int output_sum
		cdef int[:] Xi

		Xi = np.zeros((self.number_of_features,), dtype=np.int32)

		errors = 0
		for l in xrange(number_of_examples):
			###############################
			### Calculate Clause Output ###
			###############################

			for j in xrange(self.number_of_features):
				Xi[j] = X[l,j]

			self.calculate_clause_output(Xi)

			###########################
			### Sum up Clause Votes ###
			###########################

			output_sum = self.sum_up_clause_votes()
			
			if output_sum >= self.Th and y[l] == 0:
				errors += 1

			elif output_sum < self.Th and y[l] == 1:
				errors += 1

		return 1.0 - 1.0 * errors / number_of_examples

	##########################################
	### Online Training of Tsetlin Machine ###
	##########################################

	# The Tsetlin Machine can be trained incrementally, one training example at a time.
	# Use this method directly for online and incremental training.

	cpdef void update(self, int[:] X, int y):
		cdef int i, j
		cdef int action_include, action_include_negated
		cdef int output_sum

		###############################
		### Calculate Clause Output ###
		###############################

		self.calculate_clause_output(X)

		###########################
		### Sum up Clause Votes ###
		###########################

		output_sum = self.sum_up_clause_votes()

		#####################################
		### Calculate Feedback to Clauses ###
		#####################################

		# Initialize feedback to clauses
		for j in xrange(self.number_of_clauses):
			self.feedback_to_clauses[j] = 0

		if y == 1:
			# Calculate feedback to clauses
			for j in xrange(self.number_of_clauses):
				if 1.0*rand()/RAND_MAX > 1.0*(self.threshold - output_sum)/(2*self.threshold):
					continue

				if self.clause_sign[j] > 0:
					# Type I Feedback				
					self.feedback_to_clauses[j] += 1

		elif y == 0:
			for j in xrange(self.number_of_clauses):
				if 1.0*rand()/RAND_MAX > 1.0*(self.threshold + output_sum)/(2*self.threshold):
					continue

				if self.clause_sign[j] > 0:
					# Type II Feedback
					self.feedback_to_clauses[j] -= 1

	
		for j in xrange(self.number_of_clauses):
			if self.feedback_to_clauses[j] > 0:
				#######################################################
				### Type I Feedback (Combats False Negative Output) ###
				#######################################################

				if self.clause_output[j] == 0:		
					for k in xrange(self.number_of_features):	
						if 1.0*rand()/RAND_MAX <= 1.0/self.s:								
							if self.memristors[j,k,0].get_ta_state() > 1:
								self.memristors[j,k,0].tune(-self.voltage, self.dt_on)
													
						if 1.0*rand()/RAND_MAX <= 1.0/self.s:
							if self.memristors[j,k,1].get_ta_state() > 1:
								self.memristors[j,k,1].tune(-self.voltage, self.dt_on)

				if self.clause_output[j] == 1:					
					for k in xrange(self.number_of_features):
						if X[k] == 1:
							if 1.0*rand()/RAND_MAX <= 1.0*(self.s-1)/self.s:
								if self.memristors[j,k,0].get_ta_state() < self.number_of_states*2:
									self.memristors[j,k,0].tune(self.voltage, self.dt_off)

							if 1.0*rand()/RAND_MAX <= 1.0/self.s:
								if self.memristors[j,k,1].get_ta_state() > 1:
									self.memristors[j,k,1].tune(-self.voltage, self.dt_on)

						elif X[k] == 0:
							if 1.0*rand()/RAND_MAX <= 1.0*(self.s-1)/self.s:
								if self.memristors[j,k,1].get_ta_state() < self.number_of_states*2:
									self.memristors[j,k,1].tune(self.voltage, self.dt_off)

							if 1.0*rand()/RAND_MAX <= 1.0/self.s:
								if self.memristors[j,k,0].get_ta_state() > 1:
									self.memristors[j,k,0].tune(-self.voltage, self.dt_on)
					
			elif self.feedback_to_clauses[j] < 0:
				########################################################
				### Type II Feedback (Combats False Positive Output) ###
				########################################################
				if self.clause_output[j] == 1:
					for k in xrange(self.number_of_features):
						action_include = self.action(self.memristors[j,k,0].get_ta_state())
						action_include_negated = self.action(self.memristors[j,k,1].get_ta_state())

						if X[k] == 0:
							if action_include == 0 and self.memristors[j,k,0].get_ta_state() < self.number_of_states*2:
								self.memristors[j,k,0].tune(self.voltage, self.dt_off)
						elif X[k] == 1:
							if action_include_negated == 0 and self.memristors[j,k,1].get_ta_state() < self.number_of_states*2:
								self.memristors[j,k,1].tune(self.voltage, self.dt_off)
		self.append_csv()

	##############################################
	### Batch Mode Training of Tsetlin Machine ###
	##############################################

	def fit(self, int[:,:] X, int[:] y, int number_of_examples, int epochs=100):
		cdef int j, l, epoch
		cdef int example_id
		cdef int target_class
		cdef int[:] Xi
		cdef long[:] random_index
				
		Xi = np.zeros((self.number_of_features,), dtype=np.int32)
		
		random_index = np.arange(number_of_examples)

		for epoch in xrange(epochs):	
			#np.random.shuffle(random_index)

			for l in xrange(number_of_examples):
				example_id = random_index[l]
				target_class = y[example_id]

				for j in xrange(self.number_of_features):
					Xi[j] = X[example_id,j]
				self.update(Xi, target_class)

		self.close_csv()
		return
