from demo1 import File1Class

class File2Class:
    def __init__(self):
        self.file1_instance = File1Class()

    def manipulate_array(self, array):
        # ส่งค่า array ไปยังไฟล์ 1 เพื่อเพิ่มค่าที่ตำแหน่ง 0
        # manipulated_array = self.file1_instance.add_one_to_array(array)
        manipulated_array = self.File1Class.add_one_to_array(array)
        # ส่งค่าที่เพิ่มแล้วกลับมายังไฟล์ 2
        return manipulated_array

# เพื่อทดสอบการใช้งาน
if __name__ == "__main__":
    obj_file2 = File2Class()
    original_array = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    manipulated_array = obj_file2.manipulate_array(original_array)
    print(manipulated_array)  # ผลลัพธ์คือ [[1, 1, 2], [3, 4, 5], [6, 7, 8]]
