from dataclasses import dataclass

@dataclass
class Task:
    task_id: int
    device_id: int
    data_size: float
    cpu_cycles: float
    arrival_time: float = 0.0

@dataclass
class Node:
    name: str
    cpu_freq: float
    queue_time: float = 0.0
