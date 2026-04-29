import copy
import matplotlib.pyplot as plt

from config import BASELINE_CONFIG
from task_generator import generate_tasks
from simulator import MECSystem
from offloading import (
    local_policy,
    full_edge_policy,
    full_cloud_policy,
    threshold_policy,
    greedy_policy
)


def run_simulation(policy_func, config):
    system = MECSystem(config)

    tasks = generate_tasks(
        config["num_tasks"],
        config["num_devices"],
        config["task_data_min"],
        config["task_data_max"],
        config["task_cycles_min"],
        config["task_cycles_max"]
    )

    total_cost = 0.0
    total_delay = 0.0
    total_energy = 0.0

    for task in tasks:
        action = policy_func(task, system)
        result = system.execute(task, action)

        delay = result["delay"]
        energy = result["energy"]
        cost = config["alpha"] * delay + config["beta"] * energy

        total_delay += delay
        total_energy += energy
        total_cost += cost

    return total_cost, total_delay, total_energy


def plot_baseline_100_runs():
    config = copy.deepcopy(BASELINE_CONFIG)

    num_runs = 100
    run_index = list(range(1, num_runs + 1))

    local_costs = []
    edge_costs = []
    cloud_costs = []

    for _ in run_index:
        local_cost, _, _ = run_simulation(local_policy, config)
        edge_cost, _, _ = run_simulation(full_edge_policy, config)
        cloud_cost, _, _ = run_simulation(full_cloud_policy, config)

        local_costs.append(local_cost)
        edge_costs.append(edge_cost)
        cloud_costs.append(cloud_cost)

    plt.figure(figsize=(8, 4.5))
    plt.plot(run_index, local_costs, 'r-', label="Always Local")
    plt.plot(run_index, edge_costs, 'b-', label="Always Edge")
    plt.plot(run_index, cloud_costs, 'g-', label="Always Cloud")

    plt.xlabel("Simulation run")
    plt.ylabel("Total cost")
    plt.title("Baseline schemes over 100 runs")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("fig1_baseline_100runs.png", dpi=300)
    plt.show()

def plot_baseline_vs_devices():
    base = copy.deepcopy(BASELINE_CONFIG)

    device_list = [20, 40, 60, 80, 100]
    tasks_per_device = 10

    local_costs = []
    edge_costs = []
    cloud_costs = []

    for n_dev in device_list:
        config = copy.deepcopy(base)
        config["num_devices"] = n_dev
        config["num_tasks"] = n_dev * tasks_per_device

        local_cost, _, _ = run_simulation(local_policy, config)
        edge_cost, _, _ = run_simulation(full_edge_policy, config)
        cloud_cost, _, _ = run_simulation(full_cloud_policy, config)

        local_costs.append(local_cost)
        edge_costs.append(edge_cost)
        cloud_costs.append(cloud_cost)

    plt.figure(figsize=(8, 4.5))
    plt.plot(device_list, local_costs, 'r-o', label="Always Local")
    plt.plot(device_list, edge_costs, 'b-o', label="Always Edge")
    plt.plot(device_list, cloud_costs, 'g-o', label="Always Cloud")

    plt.xlabel("Number of devices")
    plt.ylabel("Total cost")
    plt.title("Baseline schemes vs system load")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("fig2_baseline_vs_devices.png", dpi=300)
    plt.show()

def plot_algorithm_100_runs():
    config = copy.deepcopy(BASELINE_CONFIG)

    num_runs = 100
    run_index = list(range(1, num_runs + 1))

    threshold_costs = []
    greedy_costs = []

    for _ in run_index:
        threshold_cost, _, _ = run_simulation(threshold_policy, config)
        greedy_cost, _, _ = run_simulation(greedy_policy, config)

        threshold_costs.append(threshold_cost)
        greedy_costs.append(greedy_cost)

    plt.figure(figsize=(8, 4.5))
    plt.plot(run_index, threshold_costs, 'c-', label="Threshold")
    plt.plot(run_index, greedy_costs, 'm-', label="Greedy")

    plt.xlabel("Simulation run")
    plt.ylabel("Total cost")
    plt.title("Threshold vs Greedy over 100 runs")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("fig3_algorithm_100runs.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_algorithm_100_runs()
    plot_baseline_vs_devices()
    plot_baseline_100_runs()
