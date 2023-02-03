import os
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.message import Message, MessageTarget
from textual.reactive import reactive, Reactive
from textual.widgets import DirectoryTree


class DirectoryDisplay(DirectoryTree):
    BINDINGS = [
        ("z", "test_binding", "Test Binding")
    ]

    def action_test_binding(self):
        self.reset_focus()

    def get_path(self) -> os.DirEntry:
        line = self._tree_lines[self.cursor_line]
        node = line.path[-1]
        return node.data


class LeftDirectoryDisplay(DirectoryDisplay):

    class ToggleDir(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    def key_right(self):
        self.emit_no_wait(self.ToggleDir(self))


class RightDirectoryDisplay(DirectoryDisplay):
    BINDINGS = [
        ("m", "move_file_dir", "Move file/dir")
    ]
    class ToggleDir(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    class Move(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    def key_left(self):
        self.emit_no_wait(self.ToggleDir(self))

    def action_move_file_dir(self):
        if self.get_path().is_dir:
            self.emit_no_wait(self.Move(self))


class DisplayContainer(Container):
    BINDINGS = [
        ("c", "close_right_screen", "Close right screen")
    ]
    path: Reactive[str] = reactive("/Users/thibauld.croonenborghs/Desktop/test")

    def compose(self) -> ComposeResult:
        yield Container(
            Container(LeftDirectoryDisplay(self.path, id="left_tree"), classes="display_container", id="left"),
            Container(classes="display_container",
                      id="right"))

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        event.stop()
        self.query_one("#left_tree_input").value = event.path

    def on_left_directory_display_toggle_dir(self, e: LeftDirectoryDisplay.ToggleDir):
        e.stop()
        try:
            right_tree = self.query_one("#right_tree")
            right_tree.focus()
        except NoMatches:
            self.query_one("#right").mount(RightDirectoryDisplay(str(Path.home()), id="right_tree"))
            self.query_one("#right_tree").focus()

    def on_right_directory_display_toggle_dir(self, e: RightDirectoryDisplay.ToggleDir):
        e.stop()
        self.query_one("#left_tree").focus()

    def action_close_right_screen(self):
        right_display = self.query_one("#right")
        right_tree = right_display.query("DirectoryDisplay")
        if right_tree:
            right_tree[0].remove()
