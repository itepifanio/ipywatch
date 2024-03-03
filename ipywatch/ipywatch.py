# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_ipywatch.ipynb.

# %% auto 0
__all__ = ['WidgetStateHistoryListener', 'Ipywatch']

# %% ../nbs/03_ipywatch.ipynb 3
from typing import Any, Callable, Optional

import ipywidgets
from comm.base_comm import BaseComm
from ipywidgets.widgets import widget as widget_module
from ipywidgets import HBox, Output, Layout

from ipywatch.history import WidgetStateHistory

# %% ../nbs/03_ipywatch.ipynb 4
class WidgetStateHistoryListener:
    def __init__(
        self,
        history_size: int = 5,
        on_state_change: Optional[Callable[[ipywidgets.Widget, Any], None]] = None
    ):
        self.history_size = history_size
        self.history = WidgetStateHistory(history_size)
        self.on_state_change = on_state_change

        _original_send = BaseComm.send

        def _patched_send(comm, data=None, metadata=None, buffers=None):
            comm_id = comm.comm_id

            widget = widget_module._instances.get(comm_id)

            self.history.set_state(comm_id, data)

            if self.on_state_change:
                self.on_state_change(widget, data)

            _original_send(comm, data, metadata, buffers)

        BaseComm.send = _patched_send  # type: ignore

# %% ../nbs/03_ipywatch.ipynb 5
class Ipywatch(HBox):
    def __init__(self, width: str = '100%', height: str = '400px', history_size: int = 5, **kwargs):
        self.updating = False  # Flag to prevent recursion
        
        self.listener = WidgetStateHistoryListener(history_size=history_size)

        self.messages = Output(layout=dict(width='100%', height='400px'))

        self.listener.on_state_change = self._on_state_change

        super().__init__(
            children=[self.messages],
            layout=Layout(width=width, height=height)
        )

    def _on_state_change(self, widget, state):
        if self.updating:
            return

        self.updating = True

        widget_type = type(widget).__name__ if widget else "Unknown"
        self.messages.append_stdout(f"Event emitted by {widget_type}: {state}\n")

        self.updating = False
