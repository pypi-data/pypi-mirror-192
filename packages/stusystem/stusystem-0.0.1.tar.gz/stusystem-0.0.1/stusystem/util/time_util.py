
import datetime
class Timer:

    def __init__(self):
        self.current_time = datetime.datetime.now()


    def show_start_time(self):
        print(self.current_time)


    def show_used_time(self):

        print( datetime.datetime.now() - self.current_time)

if __name__ == '__main__':

    t = Timer()
    t.get_used_time()