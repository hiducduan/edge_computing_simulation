class MECSystem:
    def __init__(self, config):
        self.device_cpu = config["device_cpu"]
        self.edge_cpu = config["edge_cpu"]
        self.cloud_cpu = config["cloud_cpu"]

        self.bw_de = config["bw_device_edge"]
        self.bw_ec = config["bw_edge_cloud"]

        self.power_cpu = config["power_cpu"]
        self.power_tx = config["power_tx"]

        self.alpha = config["alpha"]
        self.beta = config["beta"]

        self.num_devices = config["num_devices"]
        self.num_edges = config["num_edges"]

        # mỗi edge có một hàng đợi riêng
        self.edge_queues = [0.0 for _ in range(self.num_edges)]

        # cloud vẫn chỉ có một hàng đợi chung
        self.cloud_queue = 0.0

    def get_edge_id(self, task):
        return task.device_id % self.num_edges

    def get_devices_per_edge(self):
        return self.num_devices / self.num_edges

    def estimate(self, task, action):
        edge_id = self.get_edge_id(task)
        edge_queue = self.edge_queues[edge_id]

        # số device dùng chung edge này
        devices_per_edge = self.get_devices_per_edge()

        # bandwidth device -> edge bị chia trong phạm vi edge đó
        effective_bw_de = self.bw_de / (1.0 + 0.2 * (devices_per_edge - 1))

        if action == "local":
            proc = task.cpu_cycles / self.device_cpu
            delay = proc
            energy = self.power_cpu * proc
            return delay, energy

        elif action == "edge":
            tx = task.data_size / effective_bw_de
            proc = task.cpu_cycles / self.edge_cpu
            delay = tx + edge_queue + proc
            energy = self.power_tx * tx
            return delay, energy

        elif action == "cloud":
            tx1 = task.data_size / effective_bw_de
            tx2 = task.data_size / self.bw_ec
            proc = task.cpu_cycles / self.cloud_cpu
            delay = tx1 + tx2 + self.cloud_queue + proc
            energy = self.power_tx * (tx1 + tx2)
            return delay, energy

        else:
            raise ValueError(f"Unknown action: {action}")

    def execute(self, task, action):
        delay, energy = self.estimate(task, action)

        edge_id = self.get_edge_id(task)

        if action == "edge":
            proc = task.cpu_cycles / self.edge_cpu
            self.edge_queues[edge_id] += proc * 0.05

        elif action == "cloud":
            proc = task.cpu_cycles / self.cloud_cpu

            overload = max(0, self.num_devices - 40)

            load_factor = 1.0 + 0.15 * overload
            load_factor = min(load_factor, 7)

            self.cloud_queue += proc * 0.05 * load_factor


        # giảm queue cho từng edge
        for i in range(self.num_edges):
            self.edge_queues[i] = max(0, self.edge_queues[i] - 0.015)

        # giảm queue cloud
        self.cloud_queue = max(0, self.cloud_queue - 0.01)

        return {
            "task_id": task.task_id,
            "device_id": task.device_id,
            "edge_id": edge_id,
            "action": action,
            "delay": delay,
            "energy": energy
        }