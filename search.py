from agent import Agent
from iq import State
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
}


def handle_cli_error() -> None:
    """In the event of an unrecognized command, display all commands"""
    print("Unrecognized command. Displaying list of all commands:")
    for k, v in cmds.items():
        print(f"{k:8}{'-':4}{v[1]}")
    exit(1)


if __name__ == "__main__":
    cmd = util.get_arg(1) or None
    if not cmd:
        handle_cli_error()
    string = util.get_arg(2) or Agent.DEFAULT_STATE
    state = State(string)
    try:
        num_states = 0
        states = None
        ret = cmds.get(cmd)[0](State(string))

        # distinguish between random walk and search functions
        if isinstance(ret, tuple):

            # search fail
            if ret[1] == -1:
                print("No solution found")
                exit(0)

            # search success
            util.pprint(ret[0])
            print(ret[1])
            exit(0)

        # display random walk
        util.pprint(ret)

    except KeyError:
        handle_cli_error()
