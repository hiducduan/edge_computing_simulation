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
