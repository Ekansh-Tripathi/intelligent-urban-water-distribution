import copy

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

from graph_data import graph
from ford_fulkerson import ford_fulkerson
from water_bottleneck import (
    calculate_edge_flows,
    analyze_bottlenecks,
)


APP_VERSION = "v4"


st.set_page_config(
    page_title="Urban Water Distribution System",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 0.5rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    h1 {
        font-size: 1.8rem !important;
        margin-top: 0 !important;
        margin-bottom: 0.05rem !important;
    }

    h2 {
        font-size: 1.2rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
    }

    h3 {
        font-size: 0.95rem !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.15rem !important;
    }

    [data-testid="stMetric"] {
        padding: 0.05rem 0.15rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.45rem !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
    }

    div[data-testid="stButton"] > button {
        min-height: 2.15rem;
        padding-top: 0.1rem;
        padding-bottom: 0.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if st.session_state.get("app_version") != APP_VERSION:

    st.session_state.app_version = APP_VERSION
    st.session_state.active_graph = copy.deepcopy(graph)
    st.session_state.optimized = False
    st.session_state.flow_calculated = False
    st.session_state.show_paths = False
    st.session_state.show_bottlenecks = False
    st.session_state.optimization_result = None


if "active_graph" not in st.session_state:
    st.session_state.active_graph = copy.deepcopy(graph)

if "optimized" not in st.session_state:
    st.session_state.optimized = False

if "flow_calculated" not in st.session_state:
    st.session_state.flow_calculated = False

if "show_paths" not in st.session_state:
    st.session_state.show_paths = False

if "show_bottlenecks" not in st.session_state:
    st.session_state.show_bottlenecks = False

if "optimization_result" not in st.session_state:
    st.session_state.optimization_result = None


active_graph = st.session_state.active_graph

source = "S"
sink = "T"


# =========================================================
# GRAPH POSITIONS
# =========================================================

positions = {
    "S": (0, 2),
    "C1": (2, 4),
    "C2": (2, 2),
    "C4": (2, 0),
    "C3": (4, 4),
    "C5": (4, 2),
    "C6": (4, 0),
    "T": (6, 2),
}


# =========================================================
# ANALYSIS
# =========================================================

def calculate_analysis(current_graph):

    max_flow, flow_paths = ford_fulkerson(
        current_graph,
        source,
        sink,
    )

    edge_flows = calculate_edge_flows(
        flow_paths
    )

    analysis = analyze_bottlenecks(
        current_graph,
        edge_flows,
    )

    return (
        max_flow,
        flow_paths,
        edge_flows,
        analysis,
    )


def get_calculated_metrics(current_graph):

    (
        max_flow,
        flow_paths,
        edge_flows,
        analysis,
    ) = calculate_analysis(current_graph)

    bottleneck_count = sum(
        1
        for item in analysis
        if item["status"] == "BOTTLENECK"
    )

    utilizations = [
        item["utilization"]
        for item in analysis
    ]

    average_utilization = (
        sum(utilizations) / len(utilizations)
        if utilizations
        else 0
    )

    return {
        "max_flow": max_flow,
        "flow_paths": flow_paths,
        "edge_flows": edge_flows,
        "analysis": analysis,
        "bottlenecks": bottleneck_count,
        "average_utilization": average_utilization,
    }


# =========================================================
# DEFAULT METRICS
# =========================================================

pipeline_count = sum(
    len(active_graph[node])
    for node in active_graph
)


if st.session_state.flow_calculated:

    metrics = get_calculated_metrics(
        active_graph
    )

else:

    metrics = {
        "max_flow": None,
        "flow_paths": [],
        "edge_flows": {},
        "analysis": [],
        "bottlenecks": "--",
        "average_utilization": "--",
    }


# =========================================================
# DRAW NETWORK
# =========================================================

def draw_network(
    current_graph,
    metrics,
    show_actual_flow,
):

    figure, ax = plt.subplots(
        figsize=(8.2, 4.8),
        dpi=110,
    )

    figure.patch.set_facecolor("white")
    ax.set_facecolor("white")

    G = nx.DiGraph()

    for u in current_graph:

        for v in current_graph[u]:

            G.add_edge(
                u,
                v,
                capacity=current_graph[u][v],
            )

    bottleneck_set = set()

    if show_actual_flow:

        bottleneck_set = {
            (
                item["from"],
                item["to"],
            )
            for item in metrics["analysis"]
            if item["status"] == "BOTTLENECK"
        }

    normal_edges = []
    bottleneck_edges = []

    for u, v in G.edges():

        if (u, v) in bottleneck_set:

            bottleneck_edges.append(
                (u, v)
            )

        else:

            normal_edges.append(
                (u, v)
            )

    # -------------------------
    # Nodes
    # -------------------------

    nx.draw_networkx_nodes(
        G,
        positions,
        ax=ax,
        node_size=1650,
        node_color="skyblue",
        edgecolors="black",
        linewidths=1.4,
    )

    nx.draw_networkx_labels(
        G,
        positions,
        ax=ax,
        font_size=10,
        font_weight="bold",
    )

    # -------------------------
    # Normal edges
    # -------------------------

    if normal_edges:

        nx.draw_networkx_edges(
            G,
            positions,
            ax=ax,
            edgelist=normal_edges,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=25,
            width=2.2,
            node_size=1650,
            min_source_margin=16,
            min_target_margin=20,
        )

    # -------------------------
    # Bottleneck edges
    # -------------------------

    if bottleneck_edges:

        nx.draw_networkx_edges(
            G,
            positions,
            ax=ax,
            edgelist=bottleneck_edges,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=27,
            width=3.5,
            node_size=1650,
            edge_color="red",
            min_source_margin=16,
            min_target_margin=20,
        )

    # -------------------------
    # Edge labels
    # -------------------------

    edge_labels = {}

    for u, v in G.edges():

        capacity = current_graph[u][v]

        if show_actual_flow:

            flow = metrics["edge_flows"].get(
                (u, v),
                0,
            )

            edge_labels[(u, v)] = (
                f"{flow:g} / {capacity:g}"
            )

        else:

            edge_labels[(u, v)] = (
                f"{capacity:g}"
            )

    nx.draw_networkx_edge_labels(
        G,
        positions,
        edge_labels=edge_labels,
        ax=ax,
        font_size=9,
        label_pos=0.5,
        rotate=False,
    )

    # -------------------------
    # Title
    # -------------------------

    if st.session_state.optimized:

        state = "Optimized Network"

    else:

        state = "Original Network"

    if show_actual_flow:

        subtitle = (
            f"{state} - Actual Flow / Capacity (MLD)"
        )

    else:

        subtitle = (
            f"{state} - Pipeline Capacity (MLD)"
        )

    ax.set_title(
        "City Water Distribution Network\n"
        + subtitle,
        fontsize=14,
        fontweight="bold",
        pad=8,
    )

    ax.axis("off")
    ax.margins(0.08)

    figure.tight_layout()

    return figure


# =========================================================
# HEADER
# =========================================================

st.title(
    "URBAN WATER DISTRIBUTION AND CAPACITY OPTIMIZATION SYSTEM"
)

st.caption(
    "Ford-Fulkerson Based Water Distribution Analysis"
)


# =========================================================
# DASHBOARD
# =========================================================

card1, card2, card3, card4 = st.columns(4)


with card1:

    if st.session_state.flow_calculated:

        st.metric(
            "Maximum Flow",
            f"{metrics['max_flow']:g} MLD",
        )

    else:

        st.metric(
            "Maximum Flow",
            "-- MLD",
        )


with card2:

    st.metric(
        "Network State",
        (
            "OPTIMIZED"
            if st.session_state.optimized
            else "ORIGINAL"
        ),
    )


with card3:

    st.metric(
        "Bottlenecks",
        metrics["bottlenecks"],
    )


with card4:

    if st.session_state.flow_calculated:

        st.metric(
            "Average Utilization",
            f"{metrics['average_utilization']:.1f}%",
        )

    else:

        st.metric(
            "Average Utilization",
            "--",
        )


# =========================================================
# MAIN AREA
# =========================================================

graph_col, control_col = st.columns(
    [4.5, 1.5],
    gap="medium",
)


# =========================================================
# GRAPH
# =========================================================

with graph_col:

    st.subheader(
        "Water Distribution Network"
    )

    st.pyplot(
        draw_network(
            active_graph,
            metrics,
            st.session_state.flow_calculated,
        ),
        use_container_width=True,
    )


# =========================================================
# SYSTEM CONTROLS
# =========================================================

with control_col:

    st.subheader(
        "System Controls"
    )

    # ---------------------------------------------
    # CALCULATE MAXIMUM FLOW
    # ---------------------------------------------

    if st.button(
        "Calculate Maximum Flow",
        use_container_width=True,
    ):

        st.session_state.flow_calculated = True
        st.session_state.show_paths = False
        st.session_state.show_bottlenecks = False

        st.rerun()

    # ---------------------------------------------
    # SHOW FLOW PATHS
    # ---------------------------------------------

    if st.button(
        "Show Flow Paths",
        use_container_width=True,
    ):

        if not st.session_state.flow_calculated:

            st.warning(
                "Please calculate maximum flow first."
            )

        else:

            st.session_state.show_paths = (
                not st.session_state.show_paths
            )


    # ---------------------------------------------
    # SHOW BOTTLENECKS
    # ---------------------------------------------

    if st.button(
        "Show Bottlenecks",
        use_container_width=True,
    ):

        if not st.session_state.flow_calculated:

            st.warning(
                "Please calculate maximum flow first."
            )

        else:

            st.session_state.show_bottlenecks = (
                not st.session_state.show_bottlenecks
            )


    # ---------------------------------------------
    # NETWORK STATE
    # ---------------------------------------------

    if st.session_state.optimized:

        st.success(
            "Network: OPTIMIZED"
        )

    else:

        st.info(
            "Network: ORIGINAL"
        )


    # ---------------------------------------------
    # CAPACITY OPTIMIZATION
    # ---------------------------------------------

    st.markdown(
        "### Capacity Optimization"
    )

    pipeline_list = [
        f"{u} -> {v}"
        for u in active_graph
        for v in active_graph[u]
    ]

    selected_pipeline = st.selectbox(
        "Select Pipeline",
        pipeline_list,
        key="optimization_pipeline",
    )

    from_node, to_node = (
        selected_pipeline.split(
            " -> "
        )
    )

    current_capacity = (
        active_graph[from_node][to_node]
    )

    st.write(
        f"Current Capacity: "
        f"**{current_capacity:g} MLD**"
    )

    new_capacity = st.number_input(
        "New Capacity",
        min_value=float(
            current_capacity + 1
        ),
        value=float(
            current_capacity + 1
        ),
        step=1.0,
        key="optimization_capacity",
    )


    # ---------------------------------------------
    # PREVIEW
    # ---------------------------------------------

    if st.button(
        "Preview Optimization",
        use_container_width=True,
    ):

        if new_capacity <= current_capacity:

            st.error(
                "New capacity must be greater "
                "than current capacity."
            )

        else:

            preview_graph = copy.deepcopy(
                active_graph
            )

            preview_graph[
                from_node
            ][to_node] = new_capacity

            preview_flow, _ = ford_fulkerson(
                preview_graph,
                source,
                sink,
            )

            if st.session_state.flow_calculated:

                old_flow = metrics["max_flow"]

            else:

                old_flow, _ = ford_fulkerson(
                    active_graph,
                    source,
                    sink,
                )

            improvement = (
                preview_flow - old_flow
            )

            st.session_state.optimization_result = {

                "mode": "preview",

                "from": from_node,

                "to": to_node,

                "old_capacity":
                    current_capacity,

                "new_capacity":
                    new_capacity,

                "old_flow":
                    old_flow,

                "new_flow":
                    preview_flow,

                "improvement":
                    improvement,
            }

            st.rerun()


    # ---------------------------------------------
    # APPLY
    # ---------------------------------------------

    if st.button(
        "Apply Optimization",
        use_container_width=True,
    ):

        if new_capacity <= current_capacity:

            st.error(
                "New capacity must be greater "
                "than current capacity."
            )

        else:

            if st.session_state.flow_calculated:

                old_flow = metrics["max_flow"]

            else:

                old_flow, _ = ford_fulkerson(
                    active_graph,
                    source,
                    sink,
                )

            active_graph[
                from_node
            ][to_node] = new_capacity

            st.session_state.active_graph = (
                active_graph
            )

            st.session_state.optimized = True

            st.session_state.flow_calculated = True

            new_flow, _ = ford_fulkerson(
                active_graph,
                source,
                sink,
            )

            st.session_state.optimization_result = {

                "mode": "applied",

                "from": from_node,

                "to": to_node,

                "old_capacity":
                    current_capacity,

                "new_capacity":
                    new_capacity,

                "old_flow":
                    old_flow,

                "new_flow":
                    new_flow,

                "improvement":
                    new_flow - old_flow,
            }

            st.rerun()


    # ---------------------------------------------
    # RESET
    # ---------------------------------------------

    if st.button(
        "Reset to Original",
        use_container_width=True,
    ):

        st.session_state.active_graph = (
            copy.deepcopy(graph)
        )

        st.session_state.optimized = False

        st.session_state.flow_calculated = False

        st.session_state.show_paths = False

        st.session_state.show_bottlenecks = False

        st.session_state.optimization_result = None

        st.rerun()


# =========================================================
# FLOW PATHS
# =========================================================

if (
    st.session_state.flow_calculated
    and st.session_state.show_paths
):

    st.markdown(
        "### Ford-Fulkerson Flow Paths"
    )

    path_table = []

    for index, item in enumerate(
        metrics["flow_paths"],
        start=1,
    ):

        path_table.append(
            {
                "Step":
                    index,

                "Flow Path":
                    " → ".join(
                        item["path"]
                    ),

                "Path Flow":
                    f'{item["flow"]:g} MLD',
            }
        )

    st.dataframe(
        path_table,
        use_container_width=True,
        hide_index=True,
    )

    st.write(
        f"**Total Maximum Flow: "
        f"{metrics['max_flow']:g} MLD**"
    )


# =========================================================
# BOTTLENECKS
# =========================================================

if (
    st.session_state.flow_calculated
    and st.session_state.show_bottlenecks
):

    st.markdown(
        "### Pipeline Bottleneck Analysis"
    )

    bottleneck_table = []

    for item in metrics["analysis"]:

        bottleneck_table.append(
            {
                "Pipeline":
                    f'{item["from"]} → {item["to"]}',

                "Capacity":
                    f'{item["capacity"]} MLD',

                "Flow":
                    f'{item["flow"]} MLD',

                "Remaining":
                    f'{item["remaining"]} MLD',

                "Utilization":
                    f'{item["utilization"]:.1f}%',

                "Status":
                    item["status"],
            }
        )

    st.dataframe(
        bottleneck_table,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# OPTIMIZATION RESULT
# =========================================================

if st.session_state.optimization_result:

    result = (
        st.session_state.optimization_result
    )

    st.markdown(
        "### Optimization Result"
    )

    if result["mode"] == "preview":

        st.info(
            f"**Pipeline:** "
            f"{result['from']} → {result['to']}   |   "
            f"**Capacity:** "
            f"{result['old_capacity']:g} → "
            f"{result['new_capacity']:g} MLD   |   "
            f"**Flow:** "
            f"{result['old_flow']:g} → "
            f"{result['new_flow']:g} MLD   |   "
            f"**Expected Improvement:** "
            f"{result['improvement']:g} MLD"
        )

    else:

        st.success(
            f"**Optimization Applied**   |   "
            f"Pipeline: "
            f"{result['from']} → {result['to']}   |   "
            f"Capacity: "
            f"{result['old_capacity']:g} → "
            f"{result['new_capacity']:g} MLD   |   "
            f"Maximum Flow: "
            f"{result['old_flow']:g} → "
            f"{result['new_flow']:g} MLD   |   "
            f"Improvement: "
            f"{result['improvement']:g} MLD"
        )


# =========================================================
# FOOTER
# =========================================================

if st.session_state.flow_calculated:

    st.caption(
        f"Network State: "
        f"{'OPTIMIZED' if st.session_state.optimized else 'ORIGINAL'}"
        f" | Maximum Flow: "
        f"{metrics['max_flow']:g} MLD"
        f" | Bottlenecks: "
        f"{metrics['bottlenecks']}"
    )

else:

    st.caption(
        f"Network State: "
        f"{'OPTIMIZED' if st.session_state.optimized else 'ORIGINAL'}"
        f" | Maximum Flow: -- MLD"
        f" | Bottlenecks: --"
    )