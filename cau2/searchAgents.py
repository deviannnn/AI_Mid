from problems import PacmanProblem
import copy
import time
from queue import Queue, PriorityQueue

class searchAgents:
    def UCS(self, g: PacmanProblem) -> list:
        frontier = Queue()
        initial_state = g.pacman_pos
        frontier.put((initial_state, []))

        explored = set()
        
        while not frontier.empty():
            current_state, path = frontier.get()
            explored.add(current_state)
            #print(current_state, path)
            if g.goal_test(current_state):
                g.target_pos.discard(current_state)
                
                if not g.target_pos:
                    return path + ['Stop']
                #print("reset")
                explored.clear()
                frontier = Queue()
                frontier.put((current_state, path))
                
            for action, successor in g.get_successors(current_state):
                if successor not in explored:
                    explored.add(successor)
                    frontier.put((successor, path + [action]))
            
        return []

    def manhattan(self, current_pos, target_positions):
        return min([abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1]) for goal_pos in target_positions])

    def euclidean(self, current_pos, target_positions):
        return min([((current_pos[0] - goal_pos[0]) ** 2 + (current_pos[1] - goal_pos[1]) ** 2) ** 0.5 for goal_pos in target_positions])

    def A_star(self, g: PacmanProblem, heuristic_func) -> list:
        frontier = PriorityQueue()
        initial_state = g.pacman_pos
        f_value = heuristic_func(initial_state, g.target_pos)
        frontier.put((f_value, (initial_state, 0, [])))

        explored = set()

        while not frontier.empty():
            current_f_value, (current_state, current_g_value, path) = frontier.get()
            explored.add(current_state)
            # print('\n', current_state, 'g:', current_g_value, 'f:', current_f_value, path)
            if g.goal_test(current_state):
                g.target_pos.discard(current_state)

                if not g.target_pos:
                    return path + ['Stop']
                # print("reset")
                explored.clear()
                frontier = PriorityQueue()
                f_value = heuristic_func(current_state, g.target_pos)
                frontier.put((f_value, (current_state, 0, path)))
                continue

            for action, successor in g.get_successors(current_state):
                if successor not in explored:
                    explored.add(successor)
                    g_value = current_g_value + 1
                    h_value = heuristic_func(successor, g.target_pos)
                    f_value = g_value + h_value

                    # print("current:", current_state, ' -> ', action, ' -> ', successor, ' f:', f_value)
                    
                    frontier.put((f_value, (successor, g_value, path + [action])))

        return []

def algorithm(problem: PacmanProblem):
    searcher = searchAgents()

    searcher_chosen = int(input("Choose Searcher:\n 1.UCS \t2.A* \n"))

    if searcher_chosen == 1:
        path = searcher.UCS(problem)

    elif searcher_chosen == 2:
        heuristic_chosen = int(input("Choose Heuristic Func:\n 1.Manhattan \t 2.Euclidean\n"))

        if heuristic_chosen == 1:
            path = searcher.A_star(problem, searcher.manhattan)

        elif heuristic_chosen == 2:
            path = searcher.A_star(problem, searcher.euclidean)

        else:
            print("Manhattan is chosen as default!")
            path = searcher.A_star(problem, searcher.manhattan)

    else:
        print("UCS is chosen as default!")
        path = searcher.UCS(problem)

    print("Path:", path)
    print("Total Cost:", len(path))

    for countdown in range(3, 0, -1):
        print("Pacman will go in: ", countdown)
        time.sleep(1.25)
    
    problem.let_go_pacman(path)


while True:
    pacman = PacmanProblem()

    map_chosen = int(input("Choose Map:\n 1.Small \t 2.Medium \t 3.Big\n"))

    if map_chosen == 1:
        pacman.load_map("map/smallMaze.lay")

    elif map_chosen == 2:
        pacman.load_map("map/mediumMaze.lay")

    elif map_chosen == 3:
        pacman.load_map("map/bigMaze.lay")

    else:
        print("smallMaze is chosen as default!")
        pacman.load_map("map/smallMaze.lay")

    algorithm(pacman)