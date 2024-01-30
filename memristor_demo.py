# 1 ########################################
# # ในไลบรารี (memristor.py)
#
# import numpy as np
#
# class Memristor:
#     def __init__(self, size=(2, 2, 2)):
#         # สร้าง m_array ขนาดตามพารามิเตอร์ที่รับเข้ามา
#         self.m_array = np.round(np.random.rand(*size), 3).astype(np.float32)
#
#     def get_m_array(self):
#         return self.m_array
#
# 2 ########################################
# # # ในไลบรารี (memristor.py) สุ่มแบบกำหนดค่า
# #
# # import numpy as np
# #
# # class Memristor:
# #     def __init__(self, size=(2, 2, 2), lower_bound=1, upper_bound=2):
# #         # สร้าง m_array ขนาดตามพารามิเตอร์ที่รับเข้ามา และกำหนดช่วงค่า
# #         self.m_array = np.round(np.random.uniform(lower_bound, upper_bound, size), 3).astype(np.float32)
# #
# #     def get_m_array(self):
# #         return self.m_array
#
# 3 #########################################

import numpy as np

class Memristor:
    def __init__(self, shape, mode=0):
        self.memristor_array = np.random.choice([0.5, 0.505], size=shape)

    def get_memristor_array(self):
        return self.memristor_array, self.memristor_array * 200
