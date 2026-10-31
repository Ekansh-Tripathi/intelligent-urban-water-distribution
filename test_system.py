from graph_data import graph
from ford_fulkerson import ford_fulkerson
from bottleneck import calculate_edge_flows, analyze_bottlenecks
from optimization import optimize_capacity
from visualization import draw_graph

source = "S"
sink = "T"

max_flow, flow_paths = ford_fulkerson(graph, source, sink)

edge_flows = calculate_edge_flows(flow_paths)

analysis = analyze_bottlenecks(graph, edge_flows)

print("===================================")
print("  URBAN WATER DISTRIBUTION SYSTEM")
print("===================================")

print("Source:", source)
print("Sink:", sink)

print("\nFlow Paths:")

for item in flow_paths:
    path = " -> ".join(item["path"])
    flow = item["flow"]

    print(path, "=", flow, "MLD")

print("\nPipeline Analysis")
print("-----------------------------------------------")

for item in analysis:
    print(
        f'{item["from"]} -> {item["to"]} | '
        f'Capacity: {item["capacity"]} MLD | '
        f'Flow: {item["flow"]} MLD | '
        f'Remaining: {item["remaining"]} MLD | '
        f'Utilization: {item["utilization"]:.1f}% | '
        f'{item["status"]}'
    )

print("\nMaximum Water Flow:", max_flow, "MLD")

print("\nCapacity Optimization")
print("-----------------------------------------------")

from_node = "C6"
to_node = "T"
new_capacity = 15

result, error = optimize_capacity(
    graph,
    source,
    sink,
    from_node,
    to_node,
    new_capacity
)

if error:
    print("Error:", error)
else:
    improvement = result["new_max_flow"] - max_flow

    print(
        f'Pipeline: {from_node} -> {to_node}'
    )

    print(
        f'Old Capacity: {result["old_capacity"]} MLD'
    )

    print(
        f'New Capacity: {result["new_capacity"]} MLD'
    )

    print(
        f'Old Maximum Flow: {max_flow} MLD'
    )

    print(
        f'New Maximum Flow: {result["new_max_flow"]} MLD'
    )

    print(
        f'Improvement: {improvement} MLD'
    )
    
    print("\nOpening network graph...")
draw_graph(graph)