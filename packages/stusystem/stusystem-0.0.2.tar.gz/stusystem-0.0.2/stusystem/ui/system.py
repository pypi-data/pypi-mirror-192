
from ui.system_ui import SystemUI
from util.time_util import Timer

class System:

    def __init__(self):
        self.ui = SystemUI()
        self.timer = Timer()

    def run(self):
        self.ui.start()
        print("used time:")
        self.timer.show_used_time()

    def show_hellow_message(self):
        print("WELCOME TO SYSTEM!")
        print("current time:")
        self.timer.show_start_time()
        print()


if __name__ == '__main__':
    system = System()
    system.show_hellow_message()
    system.run()



