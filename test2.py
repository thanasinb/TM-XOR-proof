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
import time
from memristor_demo import MyClass

def main():
    # สร้างอ็อบเจ็กต์ของ MyClass
    my_object = MyClass()

    # เรียกใช้ __init__ 10 ครั้ง
    for i in range(10):
        MyClass()
        # แสดงผลจำนวนครั้งที่เรียกใช้ __init__ ในแต่ละรอบ
        print(f"รอบที่ {i + 1}: จำนวนครั้งที่เรียกใช้ __init__: {my_object.get_init_count() - 1}")

        time.sleep(1)

if __name__ == "__main__":
    main()




