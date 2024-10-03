import util


DEFAULT_STATE = 'O|OO|O-O|OOOO|OOOOO'


class Cell:
    PEG = 'O'
    EMPTY = '-'
    FORE = {'O': 'yellow', '-': 'white'}
    BACK = {'O': 'black', '-': 'black'}

    @classmethod
    def color(cls, c):
        return util.color_string(c, fore=Cell.FORE[c], back=Cell.BACK[c])


class Action:

    def __init__(self, x, y, x2, y2, xo, yo):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.xo = xo
        self.yo = yo

    def __str__(self):
        return f'jump({self.x},{self.y},{self.x2},{self.y2})'


class State:

    def __init__(self, string):
        self.board = [list(line) for line in string.split('|')]
        self.max_y = len(self.board)

    def __str__(self):
        return '|'.join([''.join(row) for row in self.board])

    def __eq__(self, state):
        return str(self) == str(state)

    def is_legal(self, x, y):
        return x >= 0 and y >= 0 and x <= y and y < self.max_y

    def get(self, x, y):
        return self.board[y][x] if self.is_legal(x, y) else None

    def row(self, y):
        return self.board[y]

    def put(self, x, y, label):
        self.board[y][x] = label

    def all_y(self):
        for y in range(self.max_y):
            yield y

    def all_x(self, y):
        for x in range(y + 1):
            yield x

    def all_xy(self):
        for y in self.all_y():
            for x in self.all_x(y):
                yield x, y

    def count_pegs(self):
        count = 0
        for x, y in self.all_xy():
            if self.get(x, y) == Cell.PEG:
                count += 1
        return count

    def is_goal(self):
        return self.count_pegs() == 1

    def get_actions(self):
        actions = []
        for x, y in self.all_xy():
            if self.get(x, y) == Cell.PEG:
                deltas = [(-1, 0), (0, +1), (+1, +1),
                          (+1, 0), (0, -1), (-1, -1)]
                for dx, dy in deltas:
                    xo, yo = x+dx, y+dy
                    x2, y2 = x+2*dx, y+2*dy
                    if (self.get(xo, yo) == Cell.PEG
                            and self.get(x2, y2) == Cell.EMPTY):
                        action = Action(x, y, x2, y2, xo, yo)
                        actions.append(action)
        actions.sort(key=lambda action: str(action))
        return actions

    def _clone(self):
        return State(str(self))

    def _execute(self, action):
        self.put(action.x, action.y, Cell.EMPTY)
        self.put(action.xo, action.yo, Cell.EMPTY)
        self.put(action.x2, action.y2, Cell.PEG)
        return self

    def execute(self, action):
        return self._clone()._execute(action)

    def pprint_string(self):
        return '\n'.join([
            ((' ' * (1 + self.max_y - len(row))) +
                util.color_string(' ', back='black').join([Cell.color(c) for c in row]) +
                (' ' * (self.max_y - len(row))))
            for row in self.board
        ])


if __name__ == '__main__':

    cmd = util.get_arg(1)

    string = util.get_arg(2) or DEFAULT_STATE
    state = State(string)

    if cmd == 'print':
        util.pprint([state])
    elif cmd == 'goal':
        print(state.is_goal())
    elif cmd == 'actions':
        for action in state.get_actions():
            print(action)
