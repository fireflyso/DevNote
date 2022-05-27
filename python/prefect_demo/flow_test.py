from prefect import task, Flow, Parameter, Task
import time
from datetime import datetime, timedelta
from prefect.executors import LocalDaskExecutor, DaskExecutor
from prefect.schedules import IntervalSchedule
import random


def send_notification(obj, old_state, new_state):
    """Sends a POST request with the error message if task fails"""
    if new_state.is_successful():
        print('{} : success'.format(obj.name))
    return new_state


schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1),
    interval=timedelta(seconds=30),
)


class MyTask(Task):
    def __init__(self, *args, info='hello', **kwargs):
        self.info = info
        super().__init__(
            *args,
            **kwargs,
            state_handlers=[send_notification],
            max_retries=3,
            retry_delay=timedelta(seconds=10),
            log_stdout=True
        )

    def run(self, parent='info'):
        print('{}: {} - {}'.format(datetime.now(), self.info, parent))
        time.sleep(random.randint(1, 3))
        return self.info


task1 = MyTask('task 01', info="task1")
task2 = MyTask('task 02', info="task2")
task3 = MyTask('task 03', info="task3")
task4 = MyTask('task 04', info="task4")
task5 = MyTask('task 05', info="task5")
task6 = MyTask('task 06', info="task6")
task7 = MyTask('task 07', info="task7")
flow = Flow(name="my_flow", tasks=[task1])
flow.add_edge(task1, task2, key='parent')
flow.add_edge(task1, task3, key='parent')
flow.add_edge(task1, task7, key='parent')
flow.add_edge(task2, task4, key='parent')
flow.add_edge(task3, task5, key='parent')
flow.add_edge([task5, task4, task7], task6, key='parent')
# flow.executor = LocalDaskExecutor()
# print("流程 ：{}".format(flow.all_downstream_edges()))
# print("任务 ：{}".format(flow.get_tasks()))
flow.executor = DaskExecutor(address="tcp://103.229.214.35:8786")
flow.run()
# flow.register('liuxulu')
