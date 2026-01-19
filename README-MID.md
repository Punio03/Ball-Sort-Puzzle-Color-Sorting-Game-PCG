# Ball Sort Puzzle Color Sorting Game + PCG
## What was already done?

In the scope of the project realization, we have implemented the key elements of the game engine and the solving algorithms. The completed tasks include:

- **Game Logic Implementation (Core Mechanics):** We created a fully functional "Ball Sort Puzzle" game environment that handles game state, ball movement rules, and victory conditions. The game is playable by executing the `run_game.py` file.
- **Human Agent:** We implemented an interface allowing for manual gameplay control by the user.
- **Agent Architecture:** We developed a base class and structure for Solver Agents, facilitating the easy addition of new algorithms.
- **Search Algorithms Implementation (Solvers):**
    - **BFS Solver:** We implemented the Breadth-First Search algorithm as a basic method for finding solutions.
    - **A\* Solver:** We implemented the A* (A-Star) algorithm with heuristics to optimize the solution search process.
- **Procedural Content Generation (PCG):** We created a Basic Random Generator that allows for the automatic creation of new, random layouts/levels to be solved.

## What changed from the initial plan?
At the current stage, the project is proceeding in accordance with the initial assumptions outlined in `README-INIT.md`. No significant changes have been made to the project's architecture or goals.

## The most important things left to do

- **Implementation of advanced PCG algorithms:** We plan to implement more sophisticated Procedural Content Generation methods, specifically focusing on Genetic Algorithms.
- **Benchmarking of generators:** We aim to create a comprehensive benchmark to evaluate and compare the quality and performance of the implemented generators.
- **Creation of a difficulty-based level pack:** We intend to generate a curated set/pack of levels with increasing difficulty to test the solvers' performance scaling.