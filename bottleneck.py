def calculate_edge_flows(flow_paths):
    edge_flows = {}

    for item in flow_paths:
        path = item["path"]
        flow = item["flow"]

        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]

            edge = (u, v)

            if edge not in edge_flows:
                edge_flows[edge] = 0

            edge_flows[edge] += flow

    return edge_flows


def analyze_bottlenecks(graph, edge_flows):
    analysis = []

    for u in graph:
        for v in graph[u]:
            capacity = graph[u][v]
            actual_flow = edge_flows.get((u, v), 0)

            remaining = capacity - actual_flow

            if capacity > 0:
                utilization = (actual_flow / capacity) * 100
            else:
                utilization = 0

            if remaining == 0:
                status = "BOTTLENECK"
            elif utilization >= 80:
                status = "HIGH UTILIZATION"
            else:
                status = "NORMAL"

            analysis.append({
                "from": u,
                "to": v,
                "capacity": capacity,
                "flow": actual_flow,
                "remaining": remaining,
                "utilization": utilization,
                "status": status
            })

    return analysis