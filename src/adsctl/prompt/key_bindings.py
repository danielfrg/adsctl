import logging

from prompt_toolkit.filters import completion_is_selected, has_completions
from prompt_toolkit.key_binding import KeyBindings

_logger = logging.getLogger(__name__)


def adsctl_bindings():
    """Custom key bindings for adsctl"""
    kb = KeyBindings()

    tab_insert_text = " " * 4

    @kb.add("tab")
    def _(event):
        """Force autocompletion at cursor on non-empty lines."""

        _logger.debug("Detected <Tab> key.")

        buff = event.app.current_buffer
        doc = buff.document

        if doc.on_first_line or doc.current_line.strip():
            if buff.complete_state:
                buff.complete_next()
            else:
                buff.start_completion(select_first=True)
        else:
            buff.insert_text(tab_insert_text, fire_event=False)

    @kb.add("escape", filter=has_completions)
    def _(event):
        """Force closing of autocompletion."""
        _logger.debug("Detected <Esc> key.")

        event.current_buffer.complete_state = None
        event.app.current_buffer.complete_state = None

    @kb.add("c-space")
    def _(event):
        """
        Initialize autocompletion at cursor.

        If the autocompletion menu is not showing, display it with the
        appropriate completions for the context.

        If the menu is showing, select the next completion.
        """
        _logger.debug("Detected <C-Space> key.")

        b = event.app.current_buffer
        if b.complete_state:
            b.complete_next()
        else:
            b.start_completion(select_first=False)

    @kb.add("enter", filter=completion_is_selected)
    def _(event):
        """Makes the enter key work as the tab key only when showing the menu.

        In other words, don't execute query when enter is pressed in
        the completion dropdown menu, instead close the dropdown menu
        (accept current selection).

        """
        _logger.debug("Detected enter key during completion selection.")

        event.current_buffer.complete_state = None
        event.app.current_buffer.complete_state = None

    return kb
