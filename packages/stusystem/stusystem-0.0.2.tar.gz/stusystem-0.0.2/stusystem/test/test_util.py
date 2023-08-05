
from model.student import Student
from model.StudentList import StudentList
from ui.system import System
from ui.system import SystemUI
from util import data_manager
from util import  time_util

def test_student():
    s = Student(no=1,name='tome',chinese =1,math = 100,english = 2)
    assert s.english == 2


def testStudentList():
    student_list = StudentList()
    student_list.load("test.txt")
    assert student_list.len() ==1


def test_system_constructor():
    system = System()
    system.show_hellow_message()

def test_systemUI_constructor():

    s=  SystemUI()

    assert s.StudentList.len() ==0


def test_datamanager_load():

    stu_list = data_manager.load("test.txt")

    assert stu_list.__len__() ==  1



def test_time_util():
    t = time_util.Timer()
    t.show_used_time()



if __name__ == '__main__':

    test_student()

    testStudentList()

    test_system_constructor()

    test_systemUI_constructor()

    test_datamanager_load()

    test_time_util()







