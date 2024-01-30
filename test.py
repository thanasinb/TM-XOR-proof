# 1
# # test.py
#
# import numpy as np
# import memritor
#
# xyz = memritor.Memristor(10,2)
#
# value_to_add = 5
# xyz.add(value_to_add)
#
# result = xyz.get_value()
#
# print(result)
# print(f"Result after adding {value_to_add}: {result}")

# 2 ######################################
# import numpy as np
#
# # สร้าง m_array ขนาด 2x2x2 ที่มีรูปแบบข้อมูลเป็น 32 บิต (float32)
# m_array_float32 = np.round(np.random.rand(2, 2, 2), 3).astype(np.float32)  # ทศนิยม 3 หลัก
#
# # แสดง m_array_float32
# print("m_array_float32:")
# print(m_array_float32)

# 3 #############################################
# ในโปรแกรมหลัก

from memristor_demo import Memristor
import memristor_demo

# สร้างอ็อบเจ็กต์ Memristor โดยระบุขนาดของ m_array
memristor_obj = Memristor(size=(2, 2, 2))

# # สร้างอ็อบเจ็กต์ Memristor โดยระบุช่วงค่าของ m_array
# memristor_obj = Memristor(size=(3, 3, 3), lower_bound=1, upper_bound=2)

# ให้ค่า m_array ที่สุ่มมาในช่วง 0 - 1
m_array_from_library = memristor_obj.get_m_array()

# แสดง m_array_from_library
print("m_array_from_library:")
print(m_array_from_library)




