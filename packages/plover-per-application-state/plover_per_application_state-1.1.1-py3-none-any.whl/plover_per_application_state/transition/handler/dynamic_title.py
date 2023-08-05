from __future__ import annotations

from plover.engine import StenoEngine

import plover_per_application_state.state.manager as _state_manager
from plover_per_application_state.transition.details import TransitionDetails
from plover_per_application_state.transition.handler.handler import TransitionHandler


class DynamicTitleTransitionHandler(TransitionHandler):

    def __init__(self, engine: StenoEngine, priority=100):
        super().__init__(engine, priority)

    def handle_transition(self, state_manager: _state_manager.StateManager,
                          engine: StenoEngine,
                          details: TransitionDetails) -> bool:
        return False
