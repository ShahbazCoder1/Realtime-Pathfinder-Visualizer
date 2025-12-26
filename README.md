# Realtime-Pathfinder-Visualizer

An interactive **Python + Pygame** application to visualize **Dijkstra’s** and **A\*** search algorithms in real time. Built as a clean, modular OOP codebase for scalability and maintainability, and optimized via efficient data structures (Priority Queues) to improve runtime.

## Highlights
- Real-time visualization of:
  - **A\*** (Manhattan heuristic)
  - **Dijkstra** (uniform-cost shortest path)
- Interactive grid editing:
  - Place **Start (S)**, **End (E)**, and **Barriers**
- User-friendly UI:
  - On-screen buttons + status bar
  - Legend for node meanings (Start/End/Barrier/Path)
- Performance-minded:
  - **PriorityQueue** + **set** membership checks + O(1) score maps (dict)  
  - Designed to support the “optimized execution time via data structure selection” claim

## Tech Stack
- Python 3.x (tested with Python 3.13)
- Pygame

## Install & Run
```bash
# 1) Install dependency
pip install pygame

# 2) Run
python main.py
```

## How to Use

### Mouse Controls
- **Left Click**
  - 1st click: place **Start (S)**  
  - 2nd click: place **End (E)**  
  - subsequent: place **Barriers**
- **Right Click**
  - remove/reset a node (including start/end)

### Buttons
- **A\* Search**: run A*
- **Dijkstra**: run Dijkstra
- **Clear Grid**: reset everything
- **Reset Path**: clears explored/path nodes but keeps barriers + start/end

### Keyboard Shortcuts
- **SPACE**: run A*
- **D**: run Dijkstra
- **C**: clear grid
- **R**: reset path (keep barriers)

## Visual Legend (Grid)
- **Start**: orange node with **S**
- **End**: cyan node with **E**
- **Barrier**: dark block
- **Open set**: light green
- **Closed set**: light pink
- **Final path**: gold

## Project Structure (actual)
```text
Realtime-Pathfinder-Visualizer/
├─ main.py         # App entry + event loop + UI wiring
├─ algorithms.py   # A* and Dijkstra implementations (Priority Queue)
├─ grid.py         # Grid creation, drawing, neighbor updates
├─ node.py         # Node model + rendering + state transitions
├─ ui.py           # Button + StatusBar UI components
├─ constants.py    # Colors, dimensions, timing (ALGORITHM_DELAY, etc.)
└─ README.md
```

## Architecture Notes (OOP + Scalability)
- **PathfinderVisualizer (main.py)** orchestrates:
  - input handling
  - grid editing
  - algorithm execution
  - rendering + UI
- **Grid / Node** separate data model + drawing responsibilities cleanly.
- **Algorithms module** is isolated so adding BFS/DFS/Greedy later is straightforward.

## Performance Notes (for resume/claims)
The implementation focuses on practical speed improvements:
- `PriorityQueue` for selecting next node (**O(log n)** push/pop).
- `set` for open-set membership (**O(1)** average).
- `dict` for distance/score tables (**O(1)** average).
These choices typically beat naive list-based scans and support a measurable speedup on larger grids.

## Troubleshooting
- Warning like:
  > `pkg_resources is deprecated as an API ...`
  This comes from Pygame’s internal dependency chain on some systems; it’s a **warning**, not a crash.
- If the window feels too large/small:
  - adjust `GRID_WIDTH`, `ROWS`, and `WINDOW_HEIGHT` in `constants.py`.

## Roadmap (optional ideas)
- Weighted grids (varying terrain cost)
- Diagonal movement toggle
- Additional algorithms (BFS/DFS/Greedy Best-First)
- Speed slider for `ALGORITHM_DELAY`
- Save/load patterns

## Contributing
1. Fork the repo
2. Create a feature branch
3. Make changes
4. Open a PR with a clear description and screenshots/video if UI-related