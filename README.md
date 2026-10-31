# Intelligent Urban Water Distribution & Capacity Optimization System

> A GUI-based intelligent water distribution system that uses the **Ford-Fulkerson maximum-flow algorithm** to analyze a directed pipeline network, identify bottlenecks, and evaluate capacity improvements.

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-Tkinter-FFB000?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/Graph-NetworkX-2C5D8A?style=for-the-badge" alt="NetworkX">
  <img src="https://img.shields.io/badge/Algorithm-Ford--Fulkerson-6A1B9A?style=for-the-badge" alt="Ford-Fulkerson">
</p>

---

## 📌 Project Overview

This project models an **urban water distribution network** as a weighted directed graph.

- **S** represents the Large Mountain Reservoir (source).
- **T** represents the Central City Water Treatment and Distribution Plant (sink).
- **C1–C6** represent regional water control stations.
- Each directed edge represents a one-way pipeline.
- Each edge capacity represents the maximum pipeline capacity in **million liters per day (MLD)**.

The system calculates the **maximum amount of water that can be transported from S to T**, identifies highly utilized pipelines, and allows the user to test capacity improvements.

---

## 🎯 Project Objectives

1. Model the given urban water network as a directed capacity graph.
2. Implement the **Ford-Fulkerson algorithm manually** for maximum-flow calculation.
3. Determine the current maximum water flow through the network.
4. Track augmenting paths and their corresponding flow values.
5. Identify pipeline bottlenecks using utilization analysis.
6. Visualize actual flow versus pipeline capacity.
7. Test capacity-upgrade scenarios and measure their impact.
8. Provide an interactive GUI for analysis and optimization.

---

## 🧠 Core Algorithm

### Ford-Fulkerson Maximum Flow

The implementation maintains a **residual graph** and repeatedly searches for an augmenting path from `S` to `T`.

For each path:

1. Find an available path from source to sink.
2. Determine the bottleneck capacity of that path.
3. Send that amount of flow through the path.
4. Update forward and reverse residual capacities.
5. Add the path flow to the total flow.
6. Continue until no augmenting path remains.

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

---

## 🗺️ Network Configuration

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

---

## ✨ Features

### 1. Maximum Flow Analysis

Calculates the maximum water flow from `S` to `T` using the custom Ford-Fulkerson implementation.

### 2. Flow Path Analysis

Displays the augmenting paths found by the algorithm and the amount of water sent through each path.

### 3. Bottleneck Detection

For every pipeline, the system reports:

- Capacity
- Actual flow
- Remaining capacity
- Utilization percentage
- Status (`BOTTLENECK`, `HIGH UTILIZATION`, or `NORMAL`)

### 4. Flow Visualization

The GUI shows:

```text
Actual Flow / Capacity
```

on each pipeline. Fully utilized bottleneck edges are highlighted visually.

### 5. Capacity Optimization

Users can select a pipeline, enter a higher capacity, preview the effect, and apply the change to the active network.

### 6. Persistent Optimization Mode

After applying an optimization:

```text
Original Network
      ↓
Apply Capacity Upgrade
      ↓
Optimized Network
      ↓
Recalculate Maximum Flow
```

The optimized network remains active until **Reset to Original** is used.

### 7. Automatic Capacity Recommendation

The system can test bottleneck improvements and recommend a pipeline upgrade scenario based on the resulting change in maximum flow.

### 8. Interactive Dashboard

The GUI provides summary indicators for:

- Maximum Flow
- Network State
- Number of Bottlenecks
- Average Network Utilization

---

## 🖥️ Technology Stack

| Technology | Purpose |
|:---|:---|
| Python | Core implementation |
| Tkinter | Desktop GUI |
| NetworkX | Directed graph representation and visualization support |
| Matplotlib | Embedded network visualization |
| Collections / `deque` | BFS queue for residual-graph search |

> **Important:** The project does **not** call a library-provided maximum-flow solver. Ford-Fulkerson is implemented in the project code.

---

## 📁 Project Structure

```text
WATER_DISTRIBUTION_PROJECT/
│
├── main.py                  # Main entry point for the standard GUI
├── gui.py                   # Stable GUI version
├── gui_optimized.py         # GUI with persistent capacity optimization
├── run_optimized.py         # Launches the optimized GUI
│
├── graph_data.py            # Network nodes, edges, and capacities
├── ford_fulkerson.py        # Custom Ford-Fulkerson implementation
├── bottleneck.py            # Edge-flow and bottleneck analysis
├── optimization.py          # Capacity optimization logic
├── visualization.py         # Standalone graph visualization
│
├── test_system.py           # Console/backend testing script
├── README.md                # Project documentation
└── Urban_Water_Distribution_Capacity_Optimization_Final_Report.docx
                               # Academic project report
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd WATER_DISTRIBUTION_PROJECT
```

### 2. Install required packages

```bash
pip install networkx matplotlib
```

> Tkinter is included with most standard Python installations on Windows. If your Python installation does not include it, install/enable Tk support for your platform.

---

## ▶️ Run the Project

### Standard GUI

```bash
python main.py
```

### Optimized GUI

```bash
python run_optimized.py
```

### Backend / Console Test

```bash
python test_system.py
```

---

## 🧪 Recommended Demo Flow

For a project demonstration, use this order:

```text
1. Open the GUI
        ↓
2. Calculate Maximum Flow
        ↓
3. Verify 29 MLD baseline
        ↓
4. Show Flow Paths
        ↓
5. Show Bottlenecks
        ↓
6. Open Capacity Optimization
        ↓
7. Preview a capacity upgrade
        ↓
8. Apply the upgrade
        ↓
9. Recalculate maximum flow
        ↓
10. Reset to Original
```

---

## 📊 Example Optimization Scenario

One tested scenario is increasing the capacity of:

```text
C6 -> T
```

from:

```text
9 MLD → 15 MLD
```

This can increase the maximum network flow from:

```text
29 MLD → 35 MLD
```

The exact improvement depends on the active capacities of the network at the time of the test.

---

## ✅ Testing Summary

The final application was checked for:

- Original maximum-flow calculation
- Flow-path display
- Bottleneck analysis
- Capacity preview
- Capacity application
- Repeated optimization on the active network
- Invalid capacity input handling
- Reset to original network
- GUI graph visualization
- Updated flow/capacity labels

Baseline validation:

```text
Original Maximum Flow = 29 MLD
```

---

## 🔍 Key Outputs

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
Current capacity → New capacity
Current maximum flow → New maximum flow
```

---

## 🚀 Future Enhancements

Possible future improvements include:

- Add/remove pipeline controls directly from the GUI.
- Simulate pipeline failures and network disruptions.
- Save/load network configurations.
- Export analysis results to CSV or PDF.
- Add cost-aware infrastructure planning.
- Compare multiple optimization scenarios side-by-side.
- Add historical demand forecasting for future water requirements.
- Add user authentication and role-based access for municipal planning teams.

---

## 📄 Documentation

The repository can include the complete academic report containing:

- Problem background
- Objectives
- Network representation
- Algorithm methodology
- GUI design
- Bottleneck analysis
- Optimization results
- Testing
- Conclusion
- Source code appendix

---

## ⭐ Project Summary

This project demonstrates how **maximum-flow algorithms can be applied to an urban water distribution network** to measure current transportation capacity, identify critical pipeline limitations, and evaluate infrastructure improvements through an interactive graphical interface.

> **Baseline network capacity: 29 MLD**

---

## 📜 License

This project is intended for **academic and educational use**.
