import random
from entities import Task

def generate_tasks(num_tasks, num_devices, data_min, data_max, cycles_min, cycles_max):
    tasks = []
    for i in range(num_tasks):
        task = Task(
            task_id=i,
            device_id=random.randint(0, num_devices - 1),
            data_size=random.uniform(data_min, data_max),
            cpu_cycles=random.uniform(cycles_min, cycles_max),
            arrival_time=i * 0.1
        )
        tasks.append(task)
    return tasks
