
import os
from model.student import Student

def save_to_file(filename,stulist):
    with open(filename, 'w', encoding='utf-8') as fp:
        for stu in stulist:
            fp.write(stu.no + ',')
            fp.write(stu.name + ',')
            fp.write(str(stu.chinese) + ',')
            fp.write(str(stu.math) + ',')
            fp.write(str(stu.english) + '\n')
        print("导出完毕")

def __exists(stulist,no):
    #判断学号是否存在
    for stu in stulist:
        if stu.no == no:
            return True
    else:
        return False

def load(filename):
    stulist = []
    # 导入学生信息
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as fp:
                while True:
                    fs = fp.readline().strip('\n')
                    if not fs:
                        break
                    else:
                        stu = Student(*fs.split(','))
                        if __exists(stu.no):
                            print('该学号已存在')
                        else:
                            stulist.append(stu)
            print('导入完毕')
        except:
            print('error...')  # 要导入的文件不是utf-8编码，或是字段数不匹配等
    else:
        print('要导入的文件不存在')
