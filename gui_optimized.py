import copy
import tkinter as tk
from tkinter import ttk, messagebox

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph_data import graph
from ford_fulkerson import ford_fulkerson
from water_bottleneck import calculate_edge_flows, analyze_bottlenecks

def create_optimized_gui():
    root = tk.Tk()

    root.title(
        "Urban Water Distribution and Capacity Optimization System"
    )

    root.geometry("1350x850")
    root.minsize(1150, 750)

    source = "S"
    sink = "T"

    original_graph = copy.deepcopy(graph)
    active_graph = copy.deepcopy(graph)

    optimized = False

    # =================================================
    # TITLE
    # =================================================

    title = tk.Label(
        root,
        text="URBAN WATER DISTRIBUTION AND CAPACITY OPTIMIZATION SYSTEM",
        font=("Arial", 20, "bold")
    )
    title.pack(pady=(15, 3))

    subtitle = tk.Label(
        root,
        text="Ford-Fulkerson Based Water Distribution Analysis",
        font=("Arial", 11)
    )
    subtitle.pack(pady=(0, 10))

    # =================================================
    # DASHBOARD
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
        text="Network State",
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
    flow_card_value.pack(pady=12)

    network_state_value = tk.Label(
        card2,
        text="ORIGINAL",
        font=("Arial", 18, "bold")
    )
    network_state_value.pack(pady=12)

    bottleneck_card_value = tk.Label(
        card3,
        text="--",
        font=("Arial", 18, "bold")
    )
    bottleneck_card_value.pack(pady=12)

    utilization_card_value = tk.Label(
        card4,
        text="-- %",
        font=("Arial", 18, "bold")
    )
    utilization_card_value.pack(pady=12)

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
    # GRAPH
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
    # DRAW NETWORK
    # =================================================

    def draw_network(
        edge_flows=None,
        analysis=None
    ):
        ax.clear()

        G = nx.DiGraph()

        for u in active_graph:
            for v in active_graph[u]:
                G.add_edge(
                    u,
                    v,
                    capacity=active_graph[u][v]
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
                bottleneck_edges.append((u, v))
            else:
                normal_edges.append((u, v))

        nx.draw_networkx_nodes(
            G,
            positions,
            ax=ax,
            node_size=1900,
            node_color="skyblue",
            edgecolors="black",
            linewidths=1.5
        )

        nx.draw_networkx_labels(
            G,
            positions,
            ax=ax,
            font_size=11,
            font_weight="bold"
        )

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

        labels = {}

        for u, v in G.edges():
            capacity = active_graph[u][v]

            if edge_flows is None:
                labels[(u, v)] = str(capacity)
            else:
                flow = edge_flows.get(
                    (u, v),
                    0
                )
                labels[(u, v)] = (
                    f"{flow:g} / {capacity:g}"
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

        if optimized:
            state_text = "Optimized Network"
        else:
            state_text = "Original Network"

        if edge_flows is None:
            ax.set_title(
                f"City Water Distribution Network\n"
                f"{state_text} - Pipeline Capacity (MLD)",
                fontsize=14,
                fontweight="bold",
                pad=15
            )
        else:
            ax.set_title(
                f"City Water Distribution Network\n"
                f"{state_text} - Actual Flow / Capacity (MLD)",
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
    # RIGHT SIDE
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

    insight_frame = tk.LabelFrame(
        right_frame,
        text="System Insight",
        font=("Arial", 10, "bold")
    )

    insight_frame.pack(
        fill="x",
        padx=10,
        pady=15
    )

    insight_label = tk.Label(
        insight_frame,
        text="Run analysis to generate insights.",
        font=("Arial", 10),
        justify="left",
        wraplength=260
    )

    insight_label.pack(
        padx=10,
        pady=10
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

    # =================================================
    # CALCULATE FLOW
    # =================================================

    def calculate_flow():
        max_flow, flow_paths = ford_fulkerson(
            active_graph,
            source,
            sink
        )

        edge_flows = calculate_edge_flows(
            flow_paths
        )

        analysis = analyze_bottlenecks(
            active_graph,
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
            text=f"{max_flow:g} MLD"
        )

        network_state_value.config(
            text="OPTIMIZED" if optimized else "ORIGINAL"
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

        insight_label.config(
            text=(
                f"Maximum water flow: "
                f"{max_flow:g} MLD.\n\n"
                f"Bottlenecks: "
                f"{bottleneck_count}.\n\n"
                f"Average utilization: "
                f"{average_utilization:.1f}%."
            )
        )

        status_label.config(
            text=(
                f"Status: Flow calculated on "
                f"{'optimized' if optimized else 'original'} network."
            )
        )

    # =================================================
    # FLOW PATHS
    # =================================================

    def show_flow_paths():
        max_flow, flow_paths = ford_fulkerson(
            active_graph,
            source,
            sink
        )

        path_window = tk.Toplevel(root)

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
        heading.pack(pady=15)

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
            text=(
                f"Total Maximum Flow: "
                f"{max_flow:g} MLD"
            ),
            font=("Arial", 13, "bold")
        )

        total_label.pack(
            pady=15
        )

    # =================================================
    # BOTTLENECKS
    # =================================================

    def show_bottlenecks():
        max_flow, flow_paths = ford_fulkerson(
            active_graph,
            source,
            sink
        )

        edge_flows = calculate_edge_flows(
            flow_paths
        )

        analysis = analyze_bottlenecks(
            active_graph,
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

        bottleneck_window = tk.Toplevel(root)

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

        heading.pack(pady=10)

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
                f"{max_flow:g} MLD"
            ),
            font=("Arial", 12, "bold")
        )

        summary.pack(pady=10)

    # =================================================
    # OPTIMIZATION WINDOW
    # =================================================

    def optimize_network():
        optimization_window = tk.Toplevel(root)

        optimization_window.title(
            "Capacity Optimization"
        )

        optimization_window.geometry(
            "700x650"
        )

        optimization_window.minsize(
            650,
            600
        )

        # -----------------------------
        # HEADER
        # -----------------------------

        heading = tk.Label(
            optimization_window,
            text="CAPACITY OPTIMIZATION",
            font=("Arial", 16, "bold")
        )

        heading.pack(
            pady=(15, 10)
        )

        # -----------------------------
        # PIPELINE
        # -----------------------------

        pipeline_label = tk.Label(
            optimization_window,
            text="Select Pipeline",
            font=("Arial", 11, "bold")
        )

        pipeline_label.pack(
            pady=(5, 5)
        )

        pipeline_list = []

        for u in active_graph:
            for v in active_graph[u]:
                pipeline_list.append(
                    f"{u} -> {v}"
                )

        pipeline_var = tk.StringVar()

        pipeline_dropdown = ttk.Combobox(
            optimization_window,
            textvariable=pipeline_var,
            values=pipeline_list,
            state="readonly",
            width=35
        )

        pipeline_dropdown.pack(
            pady=5
        )

        if pipeline_list:
            pipeline_dropdown.current(0)

        # -----------------------------
        # CURRENT CAPACITY
        # -----------------------------

        current_capacity_label = tk.Label(
            optimization_window,
            text="Current Capacity: -- MLD",
            font=("Arial", 11)
        )

        current_capacity_label.pack(
            pady=10
        )

        # -----------------------------
        # NEW CAPACITY
        # -----------------------------

        new_capacity_label = tk.Label(
            optimization_window,
            text="Enter New Capacity",
            font=("Arial", 11, "bold")
        )

        new_capacity_label.pack(
            pady=(5, 5)
        )

        new_capacity_entry = ttk.Entry(
            optimization_window,
            width=30
        )

        new_capacity_entry.pack(
            pady=5
        )

        # -----------------------------
        # RESULT AREA
        # -----------------------------

        result_frame = tk.LabelFrame(
            optimization_window,
            text="Optimization Result",
            font=("Arial", 11, "bold")
        )

        result_frame.pack(
            fill="x",
            padx=30,
            pady=15
        )

        result_text = tk.Text(
            result_frame,
            height=10,
            width=65,
            font=("Arial", 11),
            wrap="word"
        )

        result_text.pack(
            fill="x",
            padx=10,
            pady=10
        )

        result_text.config(
            state="disabled"
        )

        def set_result(text):
            result_text.config(
                state="normal"
            )

            result_text.delete(
                "1.0",
                tk.END
            )

            result_text.insert(
                tk.END,
                text
            )

            result_text.config(
                state="disabled"
            )

        # -----------------------------
        # UPDATE CURRENT CAPACITY
        # -----------------------------

        def update_current_capacity(
            event=None
        ):
            selected_pipeline = (
                pipeline_var.get()
            )

            if " -> " not in selected_pipeline:
                return

            from_node, to_node = (
                selected_pipeline.split(
                    " -> "
                )
            )

            current_capacity = (
                active_graph[from_node][to_node]
            )

            current_capacity_label.config(
                text=(
                    f"Current Capacity: "
                    f"{current_capacity:g} MLD"
                )
            )

            new_capacity_entry.delete(
                0,
                tk.END
            )

            new_capacity_entry.insert(
                0,
                str(current_capacity + 1)
            )

            set_result(
                "Enter a new capacity and click "
                "Preview Optimization."
            )

        pipeline_dropdown.bind(
            "<<ComboboxSelected>>",
            update_current_capacity
        )

        update_current_capacity()

        # -----------------------------
        # PREVIEW
        # -----------------------------

        def preview_optimization():
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
                    new_capacity_entry.get().strip()
                )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Capacity must be a number."
                )
                return

            current_capacity = (
                active_graph[from_node][to_node]
            )

            if new_capacity <= current_capacity:
                messagebox.showerror(
                    "Error",
                    (
                        "New capacity must be greater "
                        f"than current capacity "
                        f"({current_capacity:g} MLD)."
                    )
                )
                return

            preview_graph = copy.deepcopy(
                active_graph
            )

            preview_graph[from_node][to_node] = (
                new_capacity
            )

            old_flow, _ = ford_fulkerson(
                active_graph,
                source,
                sink
            )

            new_flow, _ = ford_fulkerson(
                preview_graph,
                source,
                sink
            )

            improvement = (
                new_flow - old_flow
            )

            set_result(
                f"Pipeline: {from_node} -> {to_node}\n\n"
                f"Current Capacity: "
                f"{current_capacity:g} MLD\n"
                f"New Capacity: "
                f"{new_capacity:g} MLD\n\n"
                f"Current Maximum Flow: "
                f"{old_flow:g} MLD\n"
                f"Expected Maximum Flow: "
                f"{new_flow:g} MLD\n"
                f"Expected Improvement: "
                f"{improvement:g} MLD\n\n"
                f"Preview only - network not changed."
            )

        # -----------------------------
        # APPLY
        # -----------------------------

        def apply_optimization():
            nonlocal optimized

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
                    new_capacity_entry.get().strip()
                )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Capacity must be a number."
                )
                return

            current_capacity = (
                active_graph[from_node][to_node]
            )

            if new_capacity <= current_capacity:
                messagebox.showerror(
                    "Error",
                    (
                        "New capacity must be greater "
                        f"than current capacity "
                        f"({current_capacity:g} MLD)."
                    )
                )
                return

            old_flow, _ = ford_fulkerson(
                active_graph,
                source,
                sink
            )

            # Apply the change to ACTIVE graph
            active_graph[from_node][to_node] = (
                new_capacity
            )

            new_flow, new_paths = ford_fulkerson(
                active_graph,
                source,
                sink
            )

            improvement = (
                new_flow - old_flow
            )

            optimized = True

            # Update main dashboard
            flow_card_value.config(
                text=f"{new_flow:g} MLD"
            )

            network_state_value.config(
                text="OPTIMIZED"
            )

            edge_flows = calculate_edge_flows(
                new_paths
            )

            analysis = analyze_bottlenecks(
                active_graph,
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

            insight_label.config(
                text=(
                    f"Optimization applied.\n\n"
                    f"Pipeline: "
                    f"{from_node} -> {to_node}\n"
                    f"New capacity: "
                    f"{new_capacity:g} MLD\n\n"
                    f"Maximum flow: "
                    f"{new_flow:g} MLD\n"
                    f"Improvement: "
                    f"{improvement:g} MLD"
                )
            )

            status_label.config(
                text=(
                    f"Status: Optimization applied. "
                    f"Maximum flow = "
                    f"{new_flow:g} MLD"
                )
            )

            # IMPORTANT:
            # Keep window open and update current capacity
            current_capacity_label.config(
                text=(
                    f"Current Capacity: "
                    f"{new_capacity:g} MLD"
                )
            )

            # Automatically suggest the next value
            new_capacity_entry.delete(
                0,
                tk.END
            )

            new_capacity_entry.insert(
                0,
                str(new_capacity + 1)
            )

            set_result(
                f"Pipeline: {from_node} -> {to_node}\n\n"
                f"Old Capacity: "
                f"{current_capacity:g} MLD\n"
                f"New Capacity: "
                f"{new_capacity:g} MLD\n\n"
                f"Old Maximum Flow: "
                f"{old_flow:g} MLD\n"
                f"New Maximum Flow: "
                f"{new_flow:g} MLD\n"
                f"Improvement: "
                f"{improvement:g} MLD\n\n"
                f"Optimization Applied Successfully.\n"
                f"You can enter another higher capacity "
                f"and apply again."
            )

        # -----------------------------
        # BUTTONS - ALWAYS VISIBLE
        # -----------------------------

        button_frame = tk.Frame(
            optimization_window
        )

        button_frame.pack(
            fill="x",
            padx=30,
            pady=(5, 15)
        )

        preview_button = ttk.Button(
            button_frame,
            text="Preview Optimization",
            command=preview_optimization
        )

        preview_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        apply_button = ttk.Button(
            button_frame,
            text="Apply Optimization",
            command=apply_optimization
        )

        apply_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        close_button = ttk.Button(
            button_frame,
            text="Close",
            command=optimization_window.destroy
        )

        close_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

    # =================================================
    # RESET TO ORIGINAL
    # =================================================

    def reset_system():
        nonlocal optimized

        active_graph.clear()

        for u in original_graph:
            active_graph[u] = {}

            for v in original_graph[u]:
                active_graph[u][v] = (
                    original_graph[u][v]
                )

        optimized = False

        flow_card_value.config(
            text="-- MLD"
        )

        network_state_value.config(
            text="ORIGINAL"
        )

        bottleneck_card_value.config(
            text="--"
        )

        utilization_card_value.config(
            text="-- %"
        )

        insight_label.config(
            text="Network reset to original capacities."
        )

        draw_network()

        status_label.config(
            text="Status: Original network restored."
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

    optimize_button = ttk.Button(
        right_frame,
        text="Optimize Capacity",
        command=optimize_network
    )

    optimize_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    reset_button = ttk.Button(
        right_frame,
        text="Reset to Original",
        command=reset_system
    )

    reset_button.pack(
        fill="x",
        padx=20,
        pady=6
    )

    status_label.pack(
        side="bottom",
        fill="x",
        padx=20,
        pady=8
    )

    root.mainloop()