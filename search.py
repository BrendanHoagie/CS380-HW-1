from agent import Agent
from iq import State, Cell
import util

agent = Agent()
cmds = {
    "random": [
        agent.random_walk,
        "A random walk of the state tree. Usage: random 'boardstate' (optional)",
    ],
    "bfs": [
        agent.bfs,
        "A breadth-first search of the state tree. Usage: bfs 'boardstate' (optional)",
    ],
    "dfs": [
        agent.dfs,
        "A depth-first search of the state tree. Usage: dfs 'boardstate' (optional)",
    ],
    "a_star": [
        agent.a_star,
        "An A* search of the state tree. Usage: a_star 'boardstate' (optional)",
    ],
}


def handle_cli_error() -> None:
    """In the event of an unrecognized command, display all commands"""
    print("Unrecognized command. Displaying list of all commands:")
    for k, v in cmds.items():
        print(f"{k:8}{'-':4}{v[1]}")
    exit(1)


def heuristic(state: State) -> int:
    """Heuristic function for A* search.
    The idea is to bias towards states with the most number of pegs, the most future states, and most neighbor pegs.

    Args:
        state: a State object representing the current state of the board

    Returns:
        an int representing the heuristic weight of this board state
    """
    num_pegs = state.count_pegs()
    num_future_states = len(state.get_actions())
    num_neighbor_pegs = 0
    for cur_x, cur_y in state.all_xy():
        possible_neighbors = [
            (cur_x - 1, cur_y),
            (cur_x + 1, cur_y),
            (cur_x, cur_y - 1),
            (cur_x, cur_y + 1),
        ]
        for neighbor_x, neighbor_y in possible_neighbors:
            if item := state.get(neighbor_x, neighbor_y):
                # bias strongly towards more pegs and away from empty spaces
                increase_amout = 2 if item == Cell.PEG else -1
                num_neighbor_pegs += increase_amout
    return num_pegs + num_future_states + num_neighbor_pegs


if __name__ == "__main__":
    cmd = util.get_arg(1) or None
    if not cmd:
        handle_cli_error()
    string = util.get_arg(2) or Agent.DEFAULT_STATE

    try:
        ret = 0
        states = None
        fn = cmds.get(cmd)[0]
        if fn == agent.a_star:
            ret = fn(State(string), heuristic)
        else:
            ret = fn(State(string))

        # distinguish between random walk and search functions
        if not ret:
            exit(0)

        # _search fail
        if ret == -1:
            print("No solution found")
            exit(0)

        # _search success
        print(f"{ret} iterations")

    except KeyError:
        handle_cli_error()

    except Exception as e:
        print(f"Ran into an unexpected error, exiting. Full error: {e}")
        exit(2)
