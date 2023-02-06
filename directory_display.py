import os
import shutil
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.message import Message, MessageTarget
from textual.widgets import DirectoryTree
from textual.widgets._directory_tree import DirEntry


class DirectoryDisplay(DirectoryTree):

    class ChangePath(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    # TODO: use cursor node property of tree?
    def get_path(self) -> DirEntry:
        line = self._tree_lines[self.cursor_line]
        node = line.path[-1]
        return node.data

    def key_slash(self) -> None:
        self.emit_no_wait(self.ChangePath(self))


class LeftDirectoryDisplay(DirectoryDisplay):
    BINDINGS = [
        ("->", "", "Spawn/go to right dir"),
        ("backspace", "_", "Delete file/dir")
    ]

    class ToggleDir(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    class DeleteFileDir(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    def key_right(self):
        self.emit_no_wait(self.ToggleDir(self))

    def key_backspace(self):
        self.emit_no_wait(self.DeleteFileDir(self))


class RightDirectoryDisplay(DirectoryDisplay):
    BINDINGS = [
        ("m", "move_file_dir", "Move file/dir"),
        ("<-", "", "Go to left dir")
    ]

    class ToggleDir(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    class Move(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    def key_left(self) -> None:
        self.emit_no_wait(self.ToggleDir(self))

    def action_move_file_dir(self) -> None:
        if self.get_path().is_dir:
            self.emit_no_wait(self.Move(self))


class DisplayContainer(Container):
    BINDINGS = [
        ("c", "close_right_screen", "Close right screen")
    ]

    path = "/Users/thibauld.croonenborghs/Desktop/test"

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

    def on_left_directory_display_toggle_dir(self, e: LeftDirectoryDisplay.ToggleDir) -> None:
        e.stop()
        try:
            right_tree = self.query_one("#right_tree")
            right_tree.focus()
        except NoMatches:
            self.query_one("#right").mount(RightDirectoryDisplay(str(Path.home()), id="right_tree"))
            self.query_one("#right_tree").focus()

    def on_right_directory_display_toggle_dir(self, e: RightDirectoryDisplay.ToggleDir) -> None:
        e.stop()
        self.query_one("#left_tree").focus()

    def on_left_directory_display_delete_file_dir(self, e: LeftDirectoryDisplay.DeleteFileDir) -> None:
        e.stop()
        tree: DirectoryDisplay = e.sender
        path_to_delete = tree.get_path()
        if os.path.exists(path_to_delete.path):
            if path_to_delete.is_dir:
                shutil.rmtree(path_to_delete.path)
            else:
                os.remove(path_to_delete.path)
            tree.remove()
            new_display = LeftDirectoryDisplay(tree.path, id=tree.id)
            self.query_one("#left").mount(new_display)
            new_display.focus()

    def action_close_right_screen(self) -> None:
        right_display = self.query_one("#right")
        right_tree = right_display.query("DirectoryDisplay")
        if right_tree:
            right_tree[0].remove()
