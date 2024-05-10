class File1Class:
    def add_one_to_array(self, array):
        # ตรวจสอบว่า array เป็นอาร์เรย์ของลิสต์หรือไม่
        if isinstance(array, list) and isinstance(array[0], list):
            array[0][0] += 1
        return array
