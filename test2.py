# import numpy as np
#
# class YourClass:
#     def __init__(self, number_of_clauses, number_of_features, number_of_states, s, threshold, Th):
#         self.m_array = np.zeros((2, 2, 2), dtype=np.int32)
#         print("m_array in __init__:\n", self.m_array)
#
# # สร้างอ็อบเจ็กต์ของคลาส
# your_object = YourClass(1, 1, 1, 1, 1, 1)

##########################################
# import numpy as np
#
# # สุ่มตัวเลข 0.5 หรือ 0.505
# random_array = np.random.choice([0.5, 0.505], size=(2, 2, 2))
#
# print(random_array)

#####################################
# main.py

from memristor_demo import Memristor

shape = (2, 2, 2)
# mode = 1

# สร้างอ็อบเจ็กต์ Memristor และดึง memristor_array
memristor_obj = Memristor(shape)
memristor_array = memristor_obj.get_memristor_array()


print("Memristor Array:")
print(memristor_array[0])
print("\nini_exclude:")
print(memristor_array[1])


