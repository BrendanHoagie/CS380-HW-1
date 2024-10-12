import util
import random
from iq import State
from typing_extensions import Self


class Node:

    def __init__(
        self,
        state: State = None,
        parent: Self = None,
        value: int = -1,
    ) -> None:
        self._state = state
        self._parent = parent
        self._value = value

    def get_state(self) -> State:
        """Gets the node's current state

        Returns: State
        """
        return self._state

    def set_state(self, new_state) -> None:
        """Sets the node's current state

        Args:
            new_state: a State representing the current state of this node
        """
        self._state = new_state

    def get_parent(self) -> Self:
        """Gets the node's parent

        Returns: Node | None
        """
        return self._parent

    def set_state(self, new_parent) -> None:
        """Sets the node's parent

        Args:
            new_parent: a Node representing the parent of this node
        """
        self._parent = new_parent

    def get_value(self) -> int:
        """Gets the node's value

        Returns: Int
        """
        return self._value

    def set_value(self, new_value) -> None:
        """Sets the node's current value

        Args:
            new_value: an int representing the current value of the node
        """
        self._value = new_value

    def pprint(self) -> None:
        """Print the current node data in a nice format"""
        print("State:")
        util.pprint([self._state])
        print(f"parent: {self._parent}")
        print(f"value: {self._value}")

    def get_path(self, from_root: bool = True) -> list:
        """Returns the path of this node

        Args:
            from_root: a Bool representing if the path should start from the root of the node
            tree or if the path should start from this current node

        Returns: a list of nodes in the order specified
        """
        stack = []
        lst = []
        cur = self
        while cur != None:
            stack.append(cur)
            cur = cur._parent
        if not from_root:
            return stack
        while stack != []:
            cur = stack.pop()
            lst.append(cur)
        return lst

    def print_path(self) -> None:
        """Prety prints the total path from the root to the current node"""
        util.pprint([node.get_state() for node in self.get_path(from_root=True)])


class Agent:
    DEFAULT_STATE = "O|OO|O-O|OOOO|OOOOO"

    def random_walk(self, state: State = State(DEFAULT_STATE), n: int = 8) -> list:
        """A random walk through the state space

        Args:
            state: a State object representing the starting state of the board
            n: a positive int representing the number of total possible states to be checked

        Returns: a list of States containing the path from the root
        """
        current_node = None
        prev_node = Node(state, None)
        counter = 1
        while counter < n:
            actions = state.get_actions()

            # if we've hit a dead end before checking n nodes, go back a level
            if len(actions) == 0:
                if prev_node:
                    state = prev_node.get_state()
                    continue
                print("\n\nNo more valid states\n\n")
                break

            # otherwise choose a new state
            chosen_action = actions[random.randint(0, len(actions) - 1)]
            state = state.execute(chosen_action)
            current_node = Node(state, prev_node)
            prev_node = current_node
            counter += 1

        return [node.get_state() for node in current_node.get_path(from_root=True)]
