import random

def local_policy(task, system):
    return "local"

def full_edge_policy(task, system):
    return "edge"

def full_cloud_policy(task, system):
    return "cloud"

def random_policy(task, system):
    return random.choice(["local", "edge", "cloud"])

def threshold_policy(task, system):
    # vùng task nhỏ: ưu tiên local
    if task.cpu_cycles < 1.45e9 and task.data_size < 1.55e6:
        return "local"

    # vùng task trung bình: ưu tiên edge
    elif task.cpu_cycles < 2.75e9 and task.data_size < 2.85e6:
        return "edge"

    # task nặng: cloud
    else:
        return "cloud"
    
def greedy_policy(task, system):
    options = ["local", "edge", "cloud"]
    best_action = None
    best_cost = float("inf")

    for action in options:
        delay, energy = system.estimate(task, action)
        cost = system.alpha * delay + system.beta * energy
        if cost < best_cost:
            best_cost = cost
            best_action = action

    return best_action
