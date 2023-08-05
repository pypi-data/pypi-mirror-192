

class Student:
    def __init__(self,no,name,chinese,math,english):
        self.no = no
        self.name = name
        self.chinese = int(chinese)
        self.math = int(math)
        self.english = int(english)


    def get_name(self):
        return self.name

    def get_no(self):
        return self.no

    def get_chinese(self):
        return self.chinese

    def get_math(self):
        return self.math

    def get_english(self):
        return self.english

