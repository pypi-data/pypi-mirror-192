from model.StudentList import StudentList

class SystemUI:

    def __init__(self):
        self.StudentList = StudentList()

    def infoprocess(self):
        # 基本信息管理
        print('学生基本信息管理'.center(20 ,'-'))
        print('load----------导入学生信息')
        print('insert--------添加学生信息')
        print('delete--------删除学生信息')
        print('update--------修改学生信息')
        print('show----------显示学生信息')
        print('save----------导出学生信息')
        print('return--------返回')
        print('- ' *28)
        while True:
            s = input('info>').strip().lower()
            if s == 'load':
                fn = input('请输入要导入的文件名:')
                self.StudentList.load(fn)
            elif s == 'show':
                self.StudentList.show()
            elif s == 'insert':
                self.StudentList.insert()
            elif s == 'delete':
                self.StudentList.delete()
            elif s == 'update':
                self.StudentList.update()
            elif s == 'save':
                fn = input('请输入要导出的文件名:')
                self.StudentList.save(fn)
            elif s =='return':
                break
            else:
                print('输入错误')

    def scoreprocess(self):
        # 学生成绩统计
        print('学生成绩统计'.center(24 ,'='))
        print('avg    --------课程平均分')
        print('max    --------课程最高分')
        print('min    --------课程最低分')
        print('return --------返回')
        print(''.center(30 ,'='))
        while True:
            s = input('score>').strip().lower()
            if s == 'avg':
                self.StudentList.scoreavg()
            elif s == 'max':
                self.StudentList.scoremax()
            elif s == 'min':
                self.StudentList.scoremin()
            elif s == 'return':
                break
            else:
                print('输入错误')

    def start(self):
        # 主控函数
        while True:
            print('学生信息管理系统V1.0'.center(24 ,'='))
            print('info  -------学生基本信息管理')
            print('score -------学生成绩统计')
            print('exit  -------退出系统')
            print(''.center(32 ,'='))
            s = input('main>').strip().lower()
            if s == 'info':
                self.infoprocess()
            elif s == 'score':
                self.scoreprocess()
            elif s == 'exit':
                break
            else:
                print('输入错误')

