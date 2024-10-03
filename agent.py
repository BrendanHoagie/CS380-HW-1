import util
from iq import State
from typing_extensions import Self

class Node:

	def __init__(self, state: State = None, parent: Self  = None, value: int = -1) -> None:
		self._state = state
		self._parent = parent
		self._value = value
	
	def get_state(self) -> State:
		return self._state

	def set_state(self, new_state) -> None:
		self._state = new_state

	def get_parent(self) -> Self:
		return self._parent

	def set_state(self, new_parent) -> None:
		self._parent = new_parent

	def get_value(self) -> int:
		return self._value

	def set_state(self, new_value) -> None:
		self._value = new_value

	def pprint(self) -> None:
		print("State:")
		self._state.pprint_string()
		print(f"parent: {self._parent}")  # might want to add a name tag instead of printing the parent object
		print(f"value: {self._value}")

