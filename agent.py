import util
from enum import IntEnum
import random
from iq import State
from typing_extensions import Self


class Node:

    DEFAULT_VALUE = 0

    def __init__(
        self,
        state: State = None,
        parent: Self = None,
        value: int = DEFAULT_VALUE,
    ) -> None:
        self._state = state
        self._parent = parent
        self._value = (
            value
            if value != self.DEFAULT_VALUE
            else self.DEFAULT_VALUE if not parent else parent.get_value() + 1
        )

    def get_state(self) -> State:
        """Gets the node's current state

        Returns:
            a State representing the current board state
        """
        return self._state

    def set_state(self, new_state: State) -> None:
        """Sets the node's current state

        Args:
            new_state: a State representing the current state of this node
        """
        self._state = new_state

    def get_parent(self) -> Self:
        """Gets the node's parent

        Returns:
            a Node that is the parent of this node. May be None
        """
        return self._parent

    def set_parent(self, new_parent: Self) -> None:
        """Sets the node's parent

        Args:
            new_parent: a Node representing the parent of this node

        Side Effects:
            updates the node's value to the parent's value if the new parent is not null
        """
        self._parent = new_parent
        self._value = self._parent.get_value() + 1 if self._parent else self.DEFAULT_VALUE

    def get_value(self) -> int:
        """Gets the node's value

        Returns:
            an int representing the node's current value
        """
        return self._value

    def set_value(self, new_value: int) -> None:
        """Sets the node's current value

        Args:
            new_value: an int representing the current value of the node
        """
        self._value = new_value

    def pprint(self) -> None:
        """Debug function, print the current node data in a nice format"""
        print("State:")
        util.pprint([self._state])
        print(f"parent: {self._parent}")
        print(f"value: {self._value}")

    def get_path(self, from_root: bool = True) -> list:
        """Returns the path of this node

        Args:
            from_root: a Bool representing if the path should start from the root of the node
            tree or if the path should start from this current node

        Returns:
            a list of nodes in the order specified
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


class SearchType(IntEnum):
    """An enum for the Agent class' _search function"""

    BFS = 0
    DFS = 1
    ASTAR = 2


class Agent:
    DEFAULT_STATE = "O|OO|O-O|OOOO|OOOOO"

    def _search(self, state: State, search_type: SearchType, heuristic: callable = None) -> int:
        """The main search function through the state space

        Args:
            state: a State object representing the starting state of the board
            search_type: a SearchType enum representing the type of search it should run

        Returns:
            an int tallying the total number of state nodes searched
        """

        def a_star_sort(node: Node) -> int:
            """The sort function used for A* search

            Args:
                node: a Node object representing the current node from fringe

            Returns:
                an int representing the total weight of this node's state
            """
            return node.get_value() + heuristic(node.get_state())

        closed = set()
        fringe = [Node(state)]
        cur_node = None
        num_seen = 0
        while True:
            # not done & no more unexplored nodes -> No path exists
            if not fringe:
                return -1

            # get next node
            if search_type == SearchType.ASTAR:
                fringe.sort(key=a_star_sort)
            cur_node = fringe.pop(0)
            util.pprint([node.get_state() for node in cur_node.get_path(from_root=True)])
            num_seen += 1

            # found the goal
            if cur_node.get_state().is_goal():
                break

            # this isn't the goal -> expand states
            closed.add(cur_node)
            for action in cur_node.get_state().get_actions():
                new_state = cur_node.get_state().execute(action)
                closed_states = [closed_node.get_state() for closed_node in closed]
                fringe_states = [fringe_node.get_state() for fringe_node in fringe]
                if not new_state in closed_states and not new_state in fringe_states:
                    new_node = Node(new_state, cur_node)
                    if search_type == SearchType.BFS:
                        fringe.append(new_node)
                        continue
                    if search_type == SearchType.DFS:
                        fringe.insert(0, new_node)
                        continue
                    if search_type == SearchType.ASTAR:
                        fringe.append(new_node)

        return num_seen

    def bfs(self, state: State) -> int:
        """A bfs through the state space

        Args:
            state: a State object representing the starting state of the board

        Returns:
            an int tallying the total number of state nodes searched
        """
        return self._search(state=state, search_type=SearchType.BFS)

    def dfs(self, state: State) -> int:
        """A dfs through the state space

        Args:
            state: a State object representing the starting state of the board

        Returns:
            an int tallying the total number of state nodes searched
        """
        return self._search(state=state, search_type=SearchType.DFS)

    def a_star(self, state: State, heuristic: callable) -> int:
        """A dfs through the state space

        Args:
            state: a State object representing the starting state of the board

        Returns:
            an int tallying the total number of state nodes searched
        """
        return self._search(state=state, search_type=SearchType.ASTAR, heuristic=heuristic)

    def random_walk(self, state: State = State(DEFAULT_STATE), n: int = 8) -> None:
        """A random walk through the state space

        Args:
            state: a State object representing the starting state of the board
            n: a positive int representing the number of total possible states to be checked
        """
        cur_node = None
        prev_node = Node(state, None)
        counter = 1
        while counter < n:
            actions = state.get_actions()

            # if we've hit a dead end before checking n nodes, go back a level
            if not actions:
                if prev_node and prev_node.get_state() != state:
                    state = prev_node.get_state()
                    continue

                # crash out if at end of search
                print(
                    f"Could not search {n} states, no more valid states after {counter} iterations"
                )
                util.pprint([node.get_state() for node in cur_node.get_path(from_root=True)])
                break

            # otherwise choose a new state
            chosen_action = actions[random.randint(0, len(actions) - 1)]
            state = state.execute(chosen_action)
            cur_node = Node(state, prev_node)
            prev_node = cur_node
            counter += 1

        # print the visited states as a walk from the root
        util.pprint([node.get_state() for node in cur_node.get_path(from_root=True)])
