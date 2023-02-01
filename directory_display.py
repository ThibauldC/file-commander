from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive, Reactive
from textual.widgets import DirectoryTree


class DisplayContainer(Container):
    BINDINGS = [
        ("f", "change_focus", "Change focus")
    ]
    path: Reactive[str] = reactive("/Users/thibauld.croonenborghs/Desktop/test")

    def compose(self) -> ComposeResult:
        yield Container(
            Container(LeftDirectoryDisplay(self.path, id="left_tree"), classes="display_container", id="left"),
            Container(RightDirectoryDisplay(str(Path.home()), id="right_tree"), classes="display_container",
                      id="right"))

    def action_change_focus(self):
        dd = self.query("DirectoryDisplay")
        focused = list(filter(lambda w: w.has_focus, dd))
        if focused:
            focused[0].reset_focus()
        not_focused = list(filter(lambda w: not w.has_focus, dd))
        if not_focused:
            not_focused[0].focus()


class DirectoryDisplay(DirectoryTree):
    BINDINGS = [
        ("z", "test_binding", "Test Binding")
    ]

    def action_test_binding(self):
        self.reset_focus()


class LeftDirectoryDisplay(DirectoryDisplay):
    pass


class RightDirectoryDisplay(DirectoryDisplay):
    pass
