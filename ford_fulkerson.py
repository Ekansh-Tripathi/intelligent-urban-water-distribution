from collections import deque


def bfs(residual, source, sink, parent):
    visited = set()
    queue = deque()

    queue.append(source)
    visited.add(source)

    while queue:
        u = queue.popleft()

        for v in residual[u]:
            if v not in visited and residual[u][v] > 0:
                visited.add(v)
                parent[v] = u

                if v == sink:
                    return True

                queue.append(v)

    return False


def ford_fulkerson(graph, source, sink):
    residual = {}

    for u in graph:
        residual[u] = {}

        for v in graph[u]:
            residual[u][v] = graph[u][v]

    for u in graph:
        for v in graph[u]:
            if u not in residual[v]:
                residual[v][u] = 0

    max_flow = 0
    flow_paths = []

    while True:
        parent = {}

        if not bfs(residual, source, sink, parent):
            break

        path_flow = float("inf")
        current = sink

        while current != source:
            previous = parent[current]

            path_flow = min(
                path_flow,
                residual[previous][current]
            )

            current = previous

        path = []
        current = sink

        while current != source:
            path.append(current)
            current = parent[current]

        path.append(source)
        path.reverse()

        current = sink

        while current != source:
            previous = parent[current]

            residual[previous][current] -= path_flow
            residual[current][previous] += path_flow

            current = previous

        max_flow += path_flow

        flow_paths.append({
            "path": path,
            "flow": path_flow
        })

    return max_flow, flow_paths