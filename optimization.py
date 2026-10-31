from ford_fulkerson import ford_fulkerson


def optimize_capacity(graph, source, sink, from_node, to_node, new_capacity):
    updated_graph = {}

    for u in graph:
        updated_graph[u] = {}

        for v in graph[u]:
            updated_graph[u][v] = graph[u][v]

    if from_node not in updated_graph:
        return None, "Source node does not exist."

    if to_node not in updated_graph[from_node]:
        return None, "Pipeline does not exist."

    old_capacity = updated_graph[from_node][to_node]

    if new_capacity <= old_capacity:
        return None, "New capacity must be greater than current capacity."

    updated_graph[from_node][to_node] = new_capacity

    new_max_flow, new_paths = ford_fulkerson(
        updated_graph,
        source,
        sink
    )

    return {
        "old_capacity": old_capacity,
        "new_capacity": new_capacity,
        "new_max_flow": new_max_flow,
        "new_paths": new_paths
    }, None