# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_widget_history.ipynb.

# %% auto 0
__all__ = ['WidgetStateHistory']

# %% ../nbs/02_widget_history.ipynb 3
from collections import deque
from typing import Any, Dict, Iterator

# %% ../nbs/02_widget_history.ipynb 4
class WidgetStateHistory:
    def __init__(self, history_size: int = 5):
        self.history_size = history_size
        self._widget_states: Dict[str, Any] = {}

    def set_state(self, comm_id: str, state: Any):
        if comm_id not in self._widget_states:
            self._widget_states[comm_id] = deque(maxlen=self.history_size)

        self._widget_states[comm_id].append(state)

    def get_current_state(self, comm_id: str):
        if comm_id in self._widget_states and self._widget_states[comm_id]:
            return self._widget_states[comm_id][-1]

        raise KeyError(f"No state found for widget comm_id: {comm_id}")

    def get_state_history(self, comm_id: str) -> Any:
        if comm_id in self._widget_states:
            return self._widget_states[comm_id]

        raise KeyError(f"No history found for widget comm_id: {comm_id}")

    def __setitem__(self, comm_id: str, state: Any):
        self.set_state(comm_id, state)

    def __getitem__(self, comm_id: str):
        return self.get_current_state(comm_id)

    def __delitem__(self, comm_id: str):
        if comm_id in self._widget_states:
            del self._widget_states[comm_id]
        else:
            raise KeyError(f"Comm ID {comm_id} not found")

    def __iter__(self) -> Iterator[str]:
        return iter(self._widget_states)

    def __len__(self) -> int:
        return len(self._widget_states)
