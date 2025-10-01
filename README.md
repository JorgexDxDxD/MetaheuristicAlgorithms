# AlgoRitmoAgogo

This project explores the **Airport Gate Assignment Problem (AGAP)** by implementing and comparing two metaheuristic algorithms: a **Genetic Algorithm** and a hybrid **Simulated Annealing with Tabu Search**. The goal is to efficiently assign arriving flights to airport gates or remote parking zones to minimize operational costs, specifically flight delays and gate idle time.

The project is implemented in Python within two Jupyter Notebooks:
1.  `Genetic Algorithm AGAP.ipynb`: Contains the Genetic Algorithm implementation.
2.  `Metaheuristico.py` (used by a notebook): Contains the Simulated Annealing + Tabu Search implementation.

## Algorithms

### 1. Genetic Algorithm (GA) by locoxsoco

This algorithm is inspired by the process of natural selection. It evolves a population of potential solutions over several generations to find an optimal assignment.

*   **Representation**: A solution (chromosome) is a list of flight assignments, where each gene specifies whether a flight is at a gate or a zone and its corresponding number.
*   **Fitness Function**: Evaluates the quality of a solution by calculating a cost based on:
    *   **Flight Waiting Time**: Penalty for flights that are delayed.
    *   **Gate/Zone Idle Time**: Penalty for gates and zones being unoccupied, with a higher penalty for gates.
    The fitness is the inverse of this cost, which the algorithm aims to maximize.
*   **Operators**:
    *   **Selection**: Roulette Wheel selection.
    *   **Crossover**: One-point, uniform, and permutation crossover methods are implemented.
    *   **Mutation**: Position-based and swap mutations to ensure genetic diversity.
    *   **Survival**: An elitist strategy ensures that the best solutions are carried to the next generation.

### 2. Simulated Annealing (SA) + Tabu Search (TS) by JorgexDxDxD

This hybrid algorithm models the physical process of annealing. It starts with a random solution and iteratively tries to improve it by exploring neighboring solutions.

*   **Energy Function**: Calculates the cost (energy) of a given flight assignment state, based on the same waiting time and idle time penalties as the GA. The goal is to find a state with minimum energy.
*   **Neighborhood Moves**: The algorithm explores new solutions by either:
    1.  Re-assigning a flight to a different gate/zone.
    2.  Swapping the assignments of two flights.
*   **Hybrid Strategy**:
    *   **Simulated Annealing**: The main search mechanism. It starts with a high "temperature," allowing it to accept worse solutions to escape local optima. As the temperature cools, it gradually converges towards a good solution.
    *   **Tabu Search**: This is triggered if the SA search stagnates. It uses a Tabu list to prevent recently used moves, forcing the search to explore new, unvisited areas of the solution space.

## How to Run

1.  Ensure you have the required Python libraries installed (`numpy`, `scipy`, `requests`).
2.  The input data (flight schedules) is fetched from an API or can be read from a local file (`ArrivalLima190509.txt`).
3.  Open and run the cells in `Genetic Algorithm AGAP.ipynb` to execute the Genetic Algorithm.
4.  The `Metaheuristico.py` file contains the SA+TS logic, which can be imported and run from a separate notebook to solve the same problem.

## Comparison

This project allows for a direct comparison between a population-based approach (GA) and a trajectory-based hybrid approach (SA+TS) for solving the AGAP. The GA explores the solution space broadly, while the SA+TS performs a more focused search, with mechanisms to escape local optima.
