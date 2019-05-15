import time
from multiprocessing import Process
from handle.api import app
from handle.getter import Getter
from handle.tester import Tester
from handle.setting import TESTER_ENABLED, TESTER_CYCLE, GETTER_ENABLED, GETTER_CYCLE, API_ENABLED


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run()

    def run(self):
        print('Proxy Pool starts.')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
