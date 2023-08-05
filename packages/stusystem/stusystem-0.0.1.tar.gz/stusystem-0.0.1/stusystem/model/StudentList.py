import os
from model.student import Student
from util import data_manager

class StudentList:
    def __init__(self):
        self.stulist = []
 
    def show(self):
        #显示学生信息
        print('{:8}\t{:8}\t{:8}\t{:8}\t{:8}'
              .format('学号','姓名','语文','数学','英语'))
        for stu in self.stulist:            
            print('{:8}\t{:8}\t{:<8}\t{:<8}\t{:<8}'
              .format(stu.no,stu.name,stu.chinese,stu.math,stu.english))
            
    def __enterScore(self,message):
        #成绩输入
        while True:
            try:
                score = input(message)
                if 0 <= int(score) <= 100:
                    break
                else:
                    print("输入错误，成绩应在0到100之间")
            except:
                print("输入错误，成绩应在0到100之间")
        return score  
 
    def __exists(self,no):
        #判断学号是否存在
        for stu in self.stulist:
            if stu.no == no:
                return True
        else:
            return False
        
    def insert(self):
        #添加学生信息
        while True:
            no = input('学号:')
            if self.__exists(no):
                print('该学号已存在')
            else:
                name = input('姓名:')
                chinese = self.__enterScore('语文成绩:')
                math = self.__enterScore('数学成绩:')
                english = self.__enterScore('英语成绩:')
                stu = Student(no,name,chinese,math,english)
                self.stulist.append(stu)
            choice = input('继续添加(y/n)?').lower()
            if choice == 'n':
                break
 
 
    def delete(self):
        #删除学生信息
        while True:
            no = input('请输入要删除的学生学号:')                
            for stu in self.stulist[::]:
                if stu.no == no:
                    self.stulist.remove(stu)
                    print('删除成功')
                    break
            else:
                print('该学号不存在')
            choice = input('继续删除(y/n)?').lower()
            if choice == 'n':
                break
 
 
    def update(self):
        #修改学生信息
        while True:
            no = input('请输入要修改的学生学号:')
            if self.__exists(no):
                for stu in self.stulist:
                    if stu.no == no:
                        stu.name = input('姓名:')
                        stu.chinese = int(self.__enterScore('语文成绩:'))
                        stu.math = int(self.__enterScore('数学成绩:'))
                        stu.english = int(self.__enterScore('英语成绩:'))
                        print('修改成功')
                        break
            else:
                print('该学号不存在')
            choice = input('继续修改(y/n)?').lower()
            if choice == 'n':
                break
 
    def load(self,fn):
        self.stulist = data_manager.load(fn)

 
    def save(self,fn):
        #导出学生信息
        data_manager.save_to_file(fn,self.stulist)

 
    def scoreavg(self):
        #求课程平均分
        length = len(self.stulist)
        if length > 0:
            chinese_avg = sum([stu.chinese for stu in self.stulist])/length
            math_avg = sum([stu.math for stu in self.stulist])/length
            english_avg = sum([stu.english for stu in self.stulist])/length
            print('语文成绩平均分是:%.2f'%chinese_avg)
            print('数学成绩平均分是:%.2f'%math_avg)
            print('英语成绩平均分是:%.2f'%english_avg)
        else:
            print('尚没有学生成绩...')
 
    def scoremax(self):
        #求课程最高分
        if len(self.stulist) > 0:
            chinese_max = max([stu.chinese for stu in self.stulist])
            math_max = max([stu.math for stu in self.stulist])
            english_max = max([stu.english for stu in self.stulist])
            print('语文成绩最高分是:%d'%chinese_max)
            print('数学成绩最高分是:%d'%math_max)
            print('英语成绩最高分是:%d'%english_max)
        else:
            print('尚没有学生成绩...')
 
    def scoremin(self):
        #求课程最低分
        if len(self.stulist) > 0:
            chinese_min = min([stu.chinese for stu in self.stulist])
            math_min = min([stu.math for stu in self.stulist])
            english_min = min([stu.english for stu in self.stulist])
            print('语文成绩最低分是:%d'%chinese_min)
            print('数学成绩最低分是:%d'%math_min)
            print('英语成绩最低分是:%d'%english_min)
        else:
            print('尚没有学生成绩...')
 


