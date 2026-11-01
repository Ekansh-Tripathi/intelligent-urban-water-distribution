# Intelligent Urban Water Distribution & Capacity Optimization System

A GUI-based and web-based intelligent water distribution system that uses the **Ford-Fulkerson maximum-flow algorithm** to analyze a directed pipeline network, identify bottlenecks, and evaluate pipeline capacity improvements.

## Project Overview

This project models an urban water distribution network as a weighted directed graph.

- **S** represents the Large Mountain Reservoir (source).
- **T** represents the Central City Water Treatment and Distribution Plant (sink).
- **C1-C6** represent regional water control stations.
- Each directed edge represents a one-way pipeline.
- Each edge capacity represents the maximum pipeline capacity in **million liters per day (MLD)**.

The system determines the maximum water flow that can be transported from **S to T**, identifies highly utilized pipelines, visualizes the network, and allows capacity-upgrade scenarios to be tested.

## Project Objectives

1. Model the urban water network as a directed capacity graph.
2. Implement the **Ford-Fulkerson algorithm manually** for maximum-flow calculation.
3. Determine the current maximum water flow through the network.
4. Track augmenting paths and their flow values.
5. Identify pipeline bottlenecks using utilization analysis.
6. Visualize actual flow versus pipeline capacity.
7. Test capacity-upgrade scenarios and measure their effect.
8. Provide both desktop and web-based interfaces.

## Core Algorithm

### Ford-Fulkerson Maximum Flow

The implementation maintains a **residual graph** and repeatedly searches for an augmenting path from `S` to `T`.

For each augmenting path:

1. Find an available path from source to sink.
2. Determine the minimum residual capacity on that path.
3. Send that amount of flow through the path.
4. Update forward and reverse residual capacities.
5. Add the path flow to the total flow.
6. Continue until no augmenting path remains.

The project does **not** use a library-provided maximum-flow solver.

### Baseline Result

For the provided network:

```text
Maximum Flow = 29 MLD
```

One computed set of augmenting paths is:

```text
S -> C1 -> C3 -> T    9 MLD
S -> C1 -> C5 -> T    3 MLD
S -> C2 -> C3 -> T    2 MLD
S -> C2 -> C5 -> T    6 MLD
S -> C4 -> C6 -> T    9 MLD
```

Total:

```text
9 + 3 + 2 + 6 + 9 = 29 MLD
```

## Network Configuration

| From | To | Capacity (MLD) |
|:---|:---|---:|
| S | C1 | 12 |
| S | C2 | 8 |
| S | C4 | 15 |
| C1 | C3 | 9 |
| C1 | C5 | 6 |
| C2 | C3 | 7 |
| C2 | C5 | 10 |
| C2 | C4 | 5 |
| C2 | C6 | 5 |
| C3 | T | 11 |
| C4 | C6 | 18 |
| C5 | T | 14 |
| C6 | T | 9 |

## Features

### 1. Maximum Flow Analysis

Calculates the maximum water flow from `S` to `T` using the custom Ford-Fulkerson implementation.

### 2. Flow Path Analysis

Displays the augmenting paths discovered by Ford-Fulkerson and the flow assigned to each path.

### 3. Bottleneck Detection

For each pipeline, the system can report:

- Capacity
- Actual flow
- Remaining capacity
- Utilization percentage
- Status such as `BOTTLENECK`, `HIGH UTILIZATION`, or `NORMAL`

### 4. Network Visualization

The network visualization shows either pipeline capacity or, after maximum-flow calculation, **Actual Flow / Capacity**. Fully utilized bottleneck pipelines are highlighted visually.

### 5. Capacity Optimization

Users can select a pipeline, enter a higher capacity, preview the expected impact, and apply the upgrade to the active network.

### 6. Persistent Optimization

After an optimization is applied:

```text
Original Network
       |
       v
Preview Capacity Upgrade
       |
       v
Apply Optimization
       |
       v
Optimized Network
       |
       v
Recalculate Maximum Flow
```

The optimized network remains active until **Reset to Original** is used.

### 7. Desktop GUI

The project includes a Tkinter-based desktop interface with maximum-flow calculation, flow-path display, bottleneck analysis, capacity optimization, persistent optimization, and reset functionality.

### 8. Streamlit Web Application

The project also includes a browser-based Streamlit interface with the same core analysis and optimization workflow.

Run it with:

```bash
python -m streamlit run streamlit_app.py
```

## Technology Stack

| Technology | Purpose |
|:---|:---|
| Python | Core implementation |
| Tkinter | Desktop GUI |
| Streamlit | Web interface |
| NetworkX | Directed graph representation and visualization |
| Matplotlib | Network visualization |
| `collections.deque` | BFS queue for residual-graph search |

## Project Structure

```text
WATER_DISTRIBUTION_PROJECT/
|
|-- main.py                     # Main entry point for the standard GUI
|-- gui.py                      # Stable desktop GUI
|-- gui_optimized.py            # Desktop GUI with persistent optimization
|-- run_optimized.py            # Launcher for the optimized desktop GUI
|-- streamlit_app.py            # Streamlit web application
|
|-- graph_data.py               # Network nodes, edges, and capacities
|-- ford_fulkerson.py           # Custom Ford-Fulkerson implementation
|-- water_bottleneck.py         # Edge-flow and bottleneck analysis
|-- optimization.py             # Capacity optimization logic
|-- visualization.py            # Standalone graph visualization
|
|-- test_system.py              # Console/backend testing
|-- README.md                   # Project documentation
|-- .gitignore                  # Git ignore rules
`-- Urban_Water_Distribution_Capacity_Optimization_Final_Report.docx
                                # Academic project report
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd WATER_DISTRIBUTION_PROJECT
```

### 2. Install dependencies

```bash
pip install networkx matplotlib streamlit
```

Tkinter is included with most standard Python installations on Windows. If it is not available in your Python environment, enable or install Tk support for your platform.

## Running the Project

### Standard Desktop GUI

```bash
python main.py
```

### Optimized Desktop GUI

```bash
python run_optimized.py
```

### Streamlit Web Application

```bash
python -m streamlit run streamlit_app.py
```

After starting Streamlit, open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

### Backend / Console Testing

```bash
python test_system.py
```

## Recommended Demo Flow

```text
1. Open the desktop GUI or web application
        |
        v
2. View the original network capacities
        |
        v
3. Calculate Maximum Flow
        |
        v
4. Verify the 29 MLD baseline
        |
        v
5. Show Flow Paths
        |
        v
6. Show Bottlenecks
        |
        v
7. Open Capacity Optimization
        |
        v
8. Preview a capacity upgrade
        |
        v
9. Apply the upgrade
        |
        v
10. Recalculate the optimized network
        |
        v
11. Reset to Original
```

## Example Optimization Scenario

A tested scenario increases the capacity of:

```text
C6 -> T
```

from:

```text
9 MLD -> 15 MLD
```

This scenario can increase the maximum network flow from:

```text
29 MLD -> 35 MLD
```

The actual improvement depends on the capacities of the network at the time the scenario is evaluated.

## Testing Summary

The application was checked for:

- Original maximum-flow calculation
- Flow-path display
- Bottleneck analysis
- Capacity preview
- Capacity application
- Repeated optimization on the active network
- Invalid capacity input handling
- Reset to original network
- Network visualization
- Updated flow/capacity labels

Baseline validation:

```text
Original Maximum Flow = 29 MLD
```

## Key Outputs

The system can produce:

```text
Maximum Flow: 29 MLD

Pipeline Flow / Capacity:
S -> C1    12 / 12
S -> C2     8 / 8
C1 -> C3    9 / 9
...

Bottleneck Status:
Fully utilized pipelines are identified automatically.

Optimization:
Current Capacity -> New Capacity
Current Maximum Flow -> New Maximum Flow
```

## Future Enhancements

Possible future improvements include:

- Add or remove pipeline controls directly from the interface.
- Simulate pipeline failures and network disruptions.
- Save and load network configurations.
- Export analysis results to CSV or PDF.
- Add cost-aware infrastructure planning.
- Compare multiple optimization scenarios side by side.
- Add future water-demand forecasting.
- Add municipal planning roles and access controls.

## Documentation

The academic report can contain:

- Problem background
- Project objectives
- Network representation
- Ford-Fulkerson methodology
- GUI and web interface design
- Bottleneck analysis
- Optimization results
- Testing
- Conclusion
- Source-code appendix

## Project Summary

This project demonstrates how **maximum-flow algorithms can be applied to an urban water distribution network** to measure current transportation capacity, identify critical pipeline limitations, and evaluate infrastructure improvements through interactive interfaces.

> **Baseline network capacity: 29 MLD**

## License

This project is intended for **academic and educational use**.
