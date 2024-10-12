from agent import Agent
from iq import State
import util

agent = Agent()
cmds = {
    "random": [
        agent.random_walk,
        "A random walk of the state tree. Usage: random 'boardstate' (optional)",
    ]
}


def handle_cli_error() -> None:
    """In the event of an unrecognized command, display all commands"""
    print("Unrecognized command. Displaying list of all commands")
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
        states = (cmds.get(cmd)[0])(State(string))
        util.pprint(states)

    except KeyError:
        handle_cli_error()
