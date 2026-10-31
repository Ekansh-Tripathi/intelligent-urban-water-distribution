import tkinter as tk
from tkinter import ttk, messagebox

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph_data import graph
from ford_fulkerson import ford_fulkerson
from bottleneck import calculate_edge_flows, analyze_bottlenecks
from optimization import optimize_capacity


def create_gui():
    root = tk.Tk()

    root.title(
        "Urban Water Distribution and Capacity Optimization System"
    )

    root.geometry("1350x850")
    root.minsize(1150, 750)

    source = "S"
    sink = "T"

    # =================================================
    # TITLE
    # =================================================

    title = tk.Label(
        root,
        text="URBAN WATER DISTRIBUTION AND CAPACITY OPTIMIZATION SYSTEM",
        font=("Arial", 20, "bold")
    )

    title.pack(
        pady=(15, 3)
    )

    subtitle = tk.Label(
        root,
        text="Ford-Fulkerson Based Water Distribution Analysis",
        font=("Arial", 11)
    )

    subtitle.pack(
        pady=(0, 10)
    )

    # =================================================
    # DASHBOARD CARDS
    # =================================================

    dashboard_frame = tk.Frame(root)

    dashboard_frame.pack(
        fill="x",
        padx=20,
        pady=5
    )

    card1 = tk.LabelFrame(
        dashboard_frame,
        text="Maximum Flow",
        font=("Arial", 10, "bold")
    )

    card1.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    card2 = tk.LabelFrame(
        dashboard_frame,
        text="Total Pipelines",
        font=("Arial", 10, "bold")
    )

    card2.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    card3 = tk.LabelFrame(
        dashboard_frame,
        text="Bottlenecks",
        font=("Arial", 10, "bold")
    )

    card3.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    card4 = tk.LabelFrame(
        dashboard_frame,
        text="Average Utilization",
        font=("Arial", 10, "bold")
    )

    card4.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )

    flow_card_value = tk.Label(
        card1,
        text="-- MLD",
        font=("Arial", 18, "bold")
    )

    flow_card_value.pack(
        pady=12
    )

    pipeline_count = sum(
        len(graph[u])
        for u in graph
    )

    pipeline_card_value = tk.Label(
        card2,
        text=str(pipeline_count),
        font=("Arial", 18, "bold")
    )

    pipeline_card_value.pack(
        pady=12
    )

    bottleneck_card_value = tk.Label(
        card3,
        text="--",
        font=("Arial", 18, "bold")
    )

    bottleneck_card_value.pack(
        pady=12
    )

    utilization_card_value = tk.Label(
        card4,
        text="-- %",
        font=("Arial", 18, "bold")
    )

    utilization_card_value.pack(
        pady=12
    )

    # =================================================
    # MAIN AREA
    # =================================================

    main_frame = tk.Frame(root)

    main_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    # =================================================
    # LEFT - GRAPH
    # =================================================

    left_frame = tk.LabelFrame(
        main_frame,
        text="Water Distribution Network",
        font=("Arial", 12, "bold")
    )

    left_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 10)
    )

    graph_frame = tk.Frame(left_frame)

    graph_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    figure = plt.Figure(
        figsize=(8, 6),
        dpi=100
    )

    ax = figure.add_subplot(111)

    canvas = FigureCanvasTkAgg(
        figure,
        master=graph_frame
    )

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    positions = {
        "S": (0, 2),
        "C1": (2, 4),
        "C2": (2, 2),
        "C4": (2, 0),
        "C3": (4, 4),
        "C5": (4, 2),
        "C6": (4, 0),
        "T": (6, 2)
    }

    # =================================================
    # GRAPH DRAWING
    # =================================================

    def draw_network(
        edge_flows=None,
        analysis=None
    ):
        ax.clear()

        G = nx.DiGraph()

        for u in graph:
            for v in graph[u]:
                G.add_edge(
                    u,
                    v,
                    capacity=graph[u][v]
                )

        normal_edges = []
        bottleneck_edges = []

        bottleneck_set = set()

        if analysis is not None:

            for item in analysis:

                if item["status"] == "BOTTLENECK":

                    bottleneck_set.add(
                        (
                            item["from"],
                            item["to"]
                        )
                    )

        for u, v in G.edges():

            if (u, v) in bottleneck_set:

                bottleneck_edges.append(
                    (u, v)
                )

            else:

                normal_edges.append(
                    (u, v)
                )

        # Nodes

        nx.draw_networkx_nodes(
            G,
            positions,
            ax=ax,
            node_size=1900,
            node_color="skyblue",
            edgecolors="black",
            linewidths=1.5
        )

        # Node labels

        nx.draw_networkx_labels(
            G,
            positions,
            ax=ax,
            font_size=11,
            font_weight="bold"
        )

        # Normal edges

        if normal_edges:

            nx.draw_networkx_edges(
                G,
                positions,
                ax=ax,
                edgelist=normal_edges,
                arrows=True,
                arrowstyle="-|>",
                arrowsize=28,
                width=2.5,
                node_size=1900,
                min_source_margin=18,
                min_target_margin=22
            )

        # Bottleneck edges

        if bottleneck_edges:

            nx.draw_networkx_edges(
                G,
                positions,
                ax=ax,
                edgelist=bottleneck_edges,
                arrows=True,
                arrowstyle="-|>",
                arrowsize=30,
                width=4,
                node_size=1900,
                edge_color="red",
                min_source_margin=18,
                min_target_margin=22
            )

        # Edge labels

        labels = {}

        for u, v in G.edges():

            capacity = graph[u][v]

            if edge_flows is None:

                labels[
                    (u, v)
                ] = str(capacity)

            else:

                flow = edge_flows.get(
                    (u, v),
                    0
                )

                labels[
                    (u, v)
                ] = (
                    f"{flow:g} / "
                    f"{capacity:g}"
                )

        nx.draw_networkx_edge_labels(
            G,
            positions,
            edge_labels=labels,
            ax=ax,
            font_size=10,
            label_pos=0.5,
            rotate=False
        )

        if edge_flows is None:

            ax.set_title(
                "City Water Distribution Network\n"
                "Pipeline Capacity (MLD)",
                fontsize=14,
                fontweight="bold",
                pad=15
            )

        else:

            ax.set_title(
                "City Water Distribution Network\n"
                "Actual Flow / Capacity (MLD)",
                fontsize=14,
                fontweight="bold",
                pad=15
            )

        ax.axis("off")
        ax.margins(0.15)

        figure.tight_layout()

        canvas.draw()

    draw_network()

    # =================================================
    # RIGHT - CONTROLS
    # =================================================

    right_frame = tk.LabelFrame(
        main_frame,
        text="System Controls",
        font=("Arial", 12, "bold"),
        width=330
    )

    right_frame.pack(
        side="right",
        fill="y",
        padx=(10, 0)
    )

    # =================================================
    # STATUS / RECOMMENDATION AREA
    # =================================================

    recommendation_frame = tk.LabelFrame(
        right_frame,
        text="System Insight",
        font=("Arial", 10, "bold")
    )

    recommendation_frame.pack(
        fill="x",
        padx=10,
        pady=15
    )

    recommendation_label = tk.Label(
        recommendation_frame,
        text="Run analysis to generate insights.",
        font=("Arial", 10),
        justify="left",
        wraplength=260
    )

    recommendation_label.pack(
        padx=10,
        pady=10
    )

    # =================================================
    # CALCULATE MAXIMUM FLOW
    # =================================================

    def calculate_flow():

        max_flow, flow_paths = ford_fulkerson(
            graph,
            source,
            sink
        )

        edge_flows = calculate_edge_flows(
            flow_paths
        )

        analysis = analyze_bottlenecks(
            graph,
            edge_flows
        )

        bottleneck_count = sum(
            1
            for item in analysis
            if item["status"] == "BOTTLENECK"
        )

        utilization_values = [
            item["utilization"]
            for item in analysis
        ]

        average_utilization = (
            sum(utilization_values)
            / len(utilization_values)
            if utilization_values
            else 0
        )

        flow_card_value.config(
            text=f"{max_flow} MLD"
        )

        bottleneck_card_value.config(
            text=str(bottleneck_count)
        )

        utilization_card_value.config(
            text=f"{average_utilization:.1f}%"
        )

        draw_network(
            edge_flows=edge_flows,
            analysis=analysis
        )

        recommendation_label.config(
            text=(
                f"Current maximum water flow is "
                f"{max_flow} MLD.\n\n"
                f"Detected bottlenecks: "
                f"{bottleneck_count}.\n\n"
                f"Average network utilization: "
                f"{average_utilization:.1f}%."
            )
        )

        status_label.config(
            text=(
                "Status: Maximum flow calculation completed."
            )
        )

    # =================================================
    # SHOW FLOW PATHS
    # =================================================

    def show_flow_paths():

        max_flow, flow_paths = ford_fulkerson(
            graph,
            source,
            sink
        )

        path_window = tk.Toplevel(
            root
        )

        path_window.title(
            "Ford-Fulkerson Flow Paths"
        )

        path_window.geometry(
            "700x500"
        )

        heading = tk.Label(
            path_window,
            text="FORD-FULKERSON FLOW PATHS",
            font=("Arial", 16, "bold")
        )

        heading.pack(
            pady=15
        )

        columns = (
            "Step",
            "Flow Path",
            "Path Flow"
        )

        tree = ttk.Treeview(
            path_window,
            columns=columns,
            show="headings"
        )

        tree.heading(
            "Step",
            text="Step"
        )

        tree.heading(
            "Flow Path",
            text="Flow Path"
        )

        tree.heading(
            "Path Flow",
            text="Path Flow"
        )

        tree.column(
            "Step",
            width=80,
            anchor="center"
        )

        tree.column(
            "Flow Path",
            width=400,
            anchor="center"
        )

        tree.column(
            "Path Flow",
            width=120,
            anchor="center"
        )

        for index, item in enumerate(
            flow_paths,
            start=1
        ):

            path_text = " -> ".join(
                item["path"]
            )

            tree.insert(
                "",
                "end",
                values=(
                    index,
                    path_text,
                    f'{item["flow"]:g} MLD'
                )
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        total_label = tk.Label(
            path_window,
            text=f"Total Maximum Flow: {max_flow} MLD",
            font=("Arial", 13, "bold")
        )

        total_label.pack(
            pady=15
        )

    # =================================================
    # SHOW BOTTLENECKS
    # =================================================

    def show_bottlenecks():

        max_flow, flow_paths = ford_fulkerson(
            graph,
            source,
            sink
        )

        edge_flows = calculate_edge_flows(
            flow_paths
        )

        analysis = analyze_bottlenecks(
            graph,
            edge_flows
        )

        bottleneck_count = sum(
            1
            for item in analysis
            if item["status"] == "BOTTLENECK"
        )

        bottleneck_card_value.config(
            text=str(bottleneck_count)
        )

        draw_network(
            edge_flows=edge_flows,
            analysis=analysis
        )

        bottleneck_window = tk.Toplevel(
            root
        )

        bottleneck_window.title(
            "Pipeline Bottleneck Analysis"
        )

        bottleneck_window.geometry(
            "950x550"
        )

        heading = tk.Label(
            bottleneck_window,
            text="PIPELINE BOTTLENECK ANALYSIS",
            font=("Arial", 16, "bold")
        )

        heading.pack(
            pady=10
        )

        columns = (
            "Pipeline",
            "Capacity",
            "Flow",
            "Remaining",
            "Utilization",
            "Status"
        )

        tree = ttk.Treeview(
            bottleneck_window,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=140,
                anchor="center"
            )

        for item in analysis:

            pipeline = (
                f'{item["from"]} -> '
                f'{item["to"]}'
            )

            tree.insert(
                "",
                "end",
                values=(
                    pipeline,
                    f'{item["capacity"]} MLD',
                    f'{item["flow"]} MLD',
                    f'{item["remaining"]} MLD',
                    f'{item["utilization"]:.1f}%',
                    item["status"]
                )
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        summary = tk.Label(
            bottleneck_window,
            text=(
                f"Current Maximum Flow: "
                f"{max_flow} MLD"
            ),
            font=("Arial", 12, "bold")
        )

        summary.pack(
            pady=10
        )

        recommendation_label.config(
            text=(
                f"{bottleneck_count} bottleneck "
                f"pipelines detected.\n\n"
                "Red edges in the network represent "
                "fully utilized pipelines."
            )
        )

    # =================================================
    # CAPACITY OPTIMIZATION
    # =================================================

    def optimize_network():

        old_max_flow, old_paths = ford_fulkerson(
            graph,
            source,
            sink
        )

        optimization_window = tk.Toplevel(
            root
        )

        optimization_window.title(
            "Capacity Optimization"
        )

        optimization_window.geometry(
            "600x500"
        )

        heading = tk.Label(
            optimization_window,
            text="CAPACITY OPTIMIZATION",
            font=("Arial", 16, "bold")
        )

        heading.pack(
            pady=15
        )

        pipeline_label = tk.Label(
            optimization_window,
            text="Select Pipeline",
            font=("Arial", 11, "bold")
        )

        pipeline_label.pack(
            pady=(10, 5)
        )

        pipeline_list = []

        for u in graph:

            for v in graph[u]:

                pipeline_list.append(
                    f"{u} -> {v}"
                )

        pipeline_var = tk.StringVar()

        pipeline_dropdown = ttk.Combobox(
            optimization_window,
            textvariable=pipeline_var,
            values=pipeline_list,
            state="readonly",
            width=30
        )

        pipeline_dropdown.pack(
            pady=5
        )

        if pipeline_list:

            pipeline_dropdown.current(0)

        current_capacity_label = tk.Label(
            optimization_window,
            text="Current Capacity: -- MLD",
            font=("Arial", 11)
        )

        current_capacity_label.pack(
            pady=10
        )

        new_capacity_label = tk.Label(
            optimization_window,
            text="Enter New Capacity",
            font=("Arial", 11, "bold")
        )

        new_capacity_label.pack(
            pady=(10, 5)
        )

        new_capacity_entry = ttk.Entry(
            optimization_window,
            width=25
        )

        new_capacity_entry.pack(
            pady=5
        )

        result_frame = tk.LabelFrame(
            optimization_window,
            text="Optimization Result",
            font=("Arial", 11, "bold")
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        result_label = tk.Label(
            result_frame,
            text="Enter a new capacity and click Optimize.",
            font=("Arial", 11),
            justify="left"
        )

        result_label.pack(
            padx=20,
            pady=20
        )

        def update_current_capacity(
            event=None
        ):

            selected_pipeline = pipeline_var.get()

            if " -> " not in selected_pipeline:

                return

            from_node, to_node = (
                selected_pipeline.split(
                    " -> "
                )
            )

            current_capacity = (
                graph[from_node][to_node]
            )

            current_capacity_label.config(
                text=(
                    f"Current Capacity: "
                    f"{current_capacity} MLD"
                )
            )

            new_capacity_entry.delete(
                0,
                tk.END
            )

            new_capacity_entry.insert(
                0,
                str(
                    current_capacity + 1
                )
            )

        pipeline_dropdown.bind(
            "<<ComboboxSelected>>",
            update_current_capacity
        )

        update_current_capacity()

        def apply_optimization():

            selected_pipeline = (
                pipeline_var.get()
            )

            if " -> " not in selected_pipeline:

                messagebox.showerror(
                    "Error",
                    "Please select a valid pipeline."
                )

                return

            from_node, to_node = (
                selected_pipeline.split(
                    " -> "
                )
            )

            try:

                new_capacity = float(
                    new_capacity_entry.get()
                )

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Capacity must be a number."
                )

                return

            current_capacity = (
                graph[from_node][to_node]
            )

            if new_capacity <= current_capacity:

                messagebox.showerror(
                    "Error",
                    (
                        "New capacity must be "
                        "greater than current capacity."
                    )
                )

                return

            result, error = optimize_capacity(
                graph,
                source,
                sink,
                from_node,
                to_node,
                new_capacity
            )

            if error:

                messagebox.showerror(
                    "Optimization Error",
                    error
                )

                return

            improvement = (
                result["new_max_flow"]
                - old_max_flow
            )

            result_text = (
                f"Pipeline: "
                f"{from_node} -> {to_node}\n\n"
                f"Old Capacity: "
                f"{result['old_capacity']} MLD\n\n"
                f"New Capacity: "
                f"{result['new_capacity']} MLD\n\n"
                f"Old Maximum Flow: "
                f"{old_max_flow} MLD\n\n"
                f"New Maximum Flow: "
                f"{result['new_max_flow']} MLD\n\n"
                f"Improvement: "
                f"{improvement} MLD"
            )

            result_label.config(
                text=result_text
            )

            recommendation_label.config(
                text=(
                    f"Optimization tested on "
                    f"{from_node} -> {to_node}.\n\n"
                    f"Maximum flow improved by "
                    f"{improvement} MLD."
                )
            )

        optimize_button = ttk.Button(
            optimization_window,
            text="Apply Optimization",
            command=apply_optimization
        )

        optimize_button.pack(
            pady=(0, 20)
        )

    # =================================================
    # AUTOMATIC RECOMMENDATION
    # =================================================

    def recommend_improvement():

        base_flow, base_paths = ford_fulkerson(
            graph,
            source,
            sink
        )

        edge_flows = calculate_edge_flows(
            base_paths
        )

        analysis = analyze_bottlenecks(
            graph,
            edge_flows
        )

        bottlenecks = []

        for item in analysis:

            if item["status"] == "BOTTLENECK":

                bottlenecks.append(
                    (
                        item["from"],
                        item["to"],
                        item["capacity"]
                    )
                )

        recommendation_window = tk.Toplevel(
            root
        )

        recommendation_window.title(
            "Capacity Improvement Recommendation"
        )

        recommendation_window.geometry(
            "750x550"
        )

        heading = tk.Label(
            recommendation_window,
            text="AUTOMATIC CAPACITY IMPROVEMENT",
            font=("Arial", 16, "bold")
        )

        heading.pack(
            pady=15
        )

        if not bottlenecks:

            message = tk.Label(
                recommendation_window,
                text="No bottleneck pipeline was detected.",
                font=("Arial", 13)
            )

            message.pack(
                pady=50
            )

            return

        test_increase = 5

        recommendations = []

        for (
            from_node,
            to_node,
            current_capacity
        ) in bottlenecks:

            test_capacity = (
                current_capacity
                + test_increase
            )

            result, error = optimize_capacity(
                graph,
                source,
                sink,
                from_node,
                to_node,
                test_capacity
            )

            if error:

                continue

            improvement = (
                result["new_max_flow"]
                - base_flow
            )

            recommendations.append(
                {
                    "from": from_node,
                    "to": to_node,
                    "current_capacity":
                        current_capacity,
                    "suggested_capacity":
                        test_capacity,
                    "new_flow":
                        result["new_max_flow"],
                    "improvement":
                        improvement
                }
            )

        if not recommendations:

            message = tk.Label(
                recommendation_window,
                text="No useful capacity improvement was found.",
                font=("Arial", 13)
            )

            message.pack(
                pady=50
            )

            return

        recommendations.sort(
            key=lambda x: x["improvement"],
            reverse=True
        )

        best = recommendations[0]

        result_frame = tk.LabelFrame(
            recommendation_window,
            text="Recommended Improvement",
            font=("Arial", 12, "bold")
        )

        result_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )

        recommendation_text = (
            f"Recommended Pipeline: "
            f"{best['from']} -> {best['to']}\n\n"
            f"Current Capacity: "
            f"{best['current_capacity']} MLD\n\n"
            f"Suggested Capacity: "
            f"{best['suggested_capacity']} MLD\n\n"
            f"Current Maximum Flow: "
            f"{base_flow} MLD\n\n"
            f"Expected Maximum Flow: "
            f"{best['new_flow']} MLD\n\n"
            f"Expected Improvement: "
            f"{best['improvement']} MLD"
        )

        result_label = tk.Label(
            result_frame,
            text=recommendation_text,
            font=("Arial", 12),
            justify="left"
        )

        result_label.pack(
            padx=25,
            pady=25
        )

        recommendation_label.config(
            text=(
                f"Recommended pipeline: "
                f"{best['from']} -> {best['to']}.\n\n"
                f"Expected improvement: "
                f"{best['improvement']} MLD."
            )
        )

    # =================================================
    # RESET
    # =================================================

    def reset_system():

        flow_card_value.config(
            text="-- MLD"
        )

        bottleneck_card_value.config(
            text="--"
        )

        utilization_card_value.config(
            text="-- %"
        )

        recommendation_label.config(
            text="Run analysis to generate insights."
        )

        draw_network()

        status_label.config(
            text="Status: Ready"
        )

    # =================================================
    # BUTTONS
    # =================================================

    calculate_button = ttk.Button(
        right_frame,
        text="Calculate Maximum Flow",
        command=calculate_flow
    )

    calculate_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    flow_paths_button = ttk.Button(
        right_frame,
        text="Show Flow Paths",
        command=show_flow_paths
    )

    flow_paths_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    bottleneck_button = ttk.Button(
        right_frame,
        text="Show Bottlenecks",
        command=show_bottlenecks
    )

    bottleneck_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    recommendation_button = ttk.Button(
        right_frame,
        text="Recommend Improvement",
        command=recommend_improvement
    )

    recommendation_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    optimization_button = ttk.Button(
        right_frame,
        text="Optimize Capacity",
        command=optimize_network
    )

    optimization_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    reset_button = ttk.Button(
        right_frame,
        text="Reset",
        command=reset_system
    )

    reset_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    # =================================================
    # STATUS BAR
    # =================================================

    status_label = tk.Label(
        root,
        text="Status: Ready",
        anchor="w",
        font=("Arial", 10)
    )

    status_label.pack(
        side="bottom",
        fill="x",
        padx=20,
        pady=8
    )

    root.mainloop()