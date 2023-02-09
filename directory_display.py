from enum import Enum
import os
import shutil
from pathlib import Path

from rich.syntax import Syntax
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.css.query import NoMatches
from textual.message import Message, MessageTarget
from textual.widgets import DirectoryTree, TreeNode, Static
from textual.widgets._directory_tree import DirEntry


class Change(Enum):
    NewFile = "new_file"
    NewDir = "new_dir"
    ChangePath = "change_path"
    Rename = "rename"
    Delete = "delete"


class DirectoryDisplay(DirectoryTree):

    class ChangeEvent(Message):
        def __init__(self, sender: MessageTarget, event: Change):
            self.event = event
            super().__init__(sender)

    def get_current_node_entry(self) -> DirEntry:
        line = self._tree_lines[self.cursor_line]
        node = line.path[-1]
        return node.data

    def clear(self) -> None:
        """Clear all nodes under root."""
        self._line_cache.clear()
        self._tree_lines_cached = None
        self._current_id = 0
        root_label = self.root._label
        root_data = self.root.data
        self.root = TreeNode(
            self,
            None,
            self._new_id(),
            root_label,
            root_data,
            expanded=True,
        )
        self._updates += 1
        self.refresh()

    # TODO: replace by reset() and load_directory when the change is included in the next release of textual: https://github.com/Textualize/textual/pull/1709/files
    def refresh_path(self):
        self.clear()
        self.root.label = Text(self.path)
        self.root.data = DirEntry(self.path, True)
        self.load_directory(self.root)

    def key_slash(self) -> None:
        self.emit_no_wait(self.ChangeEvent(self, Change.ChangePath))


class LeftDirectoryDisplay(DirectoryDisplay):
    BINDINGS = [
        ("->", "", "Spawn/go to right dir"),
        ("backspace", "_", "Delete"),
        ("n", "add_file", "Add file"),
        ("d", "add_dir", "Add dir"),
        ("r", "rename", "Rename"),
        ("shift+->", "__", "Code view")
    ]

    class ToggleDir(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    class ToggleCode(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    def key_right(self):
        self.emit_no_wait(self.ToggleDir(self))

    def key_backspace(self):
        self.emit_no_wait(self.ChangeEvent(self, Change.Delete))

    def key_shift_right(self):
        self.emit_no_wait(self.ToggleCode(self))

    def action_add_file(self):
        self.emit_no_wait(self.ChangeEvent(self, Change.NewFile))

    def action_add_dir(self):
        self.emit_no_wait(self.ChangeEvent(self, Change.NewDir))

    def action_rename(self):
        self.emit_no_wait(self.ChangeEvent(self, Change.Rename))


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
        if self.get_current_node_entry().is_dir:
            self.emit_no_wait(self.Move(self))


class DisplayContainer(Container):
    BINDINGS = [
        ("c", "close_right_screen", "Close right screen")
    ]

    path = "/Users/thibauld.croonenborghs/Desktop/test"

    def compose(self) -> ComposeResult:
        yield Container(
            Container(LeftDirectoryDisplay(self.path, id="left_tree"), classes="display_container", id="left"),
            Container(classes="display_container", id="right"))

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
            if self.query_one("#right").query("#code"):
                self.query_one("#right").query_one("#code").remove()
            self.query_one("#right").mount(RightDirectoryDisplay(str(Path.home()), id="right_tree"))
            self.query_one("#right_tree").focus()

    def on_left_directory_display_toggle_code(self, e: LeftDirectoryDisplay.ToggleCode) -> None:
        e.stop()
        try:
            code_view = self.query_one("#code_view")
        except NoMatches:
            if self.query_one("#right").query("#right_tree"):
                self.query_one("#right").query_one("#right_tree").remove()
            self.query_one("#right").mount(Vertical(Static(id="code_view", expand=True), id="code"))
            code_view = self.query_one("#code_view")

        current_node = e.sender.get_current_node_entry()
        if not current_node.is_dir:
            syntax = Syntax.from_path(
                current_node.path,
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
            code_view.update(syntax)
            code_view.scroll_home(animate=False)

    def on_right_directory_display_toggle_dir(self, e: RightDirectoryDisplay.ToggleDir) -> None:
        e.stop()
        self.query_one("#left_tree").focus()

    @staticmethod
    def on_directory_display_change_event(e: DirectoryDisplay.ChangeEvent) -> None:
        if e.event == Change.Delete:
            e.stop()
            tree: DirectoryDisplay = e.sender
            path_to_delete = tree.get_current_node_entry()
            if os.path.exists(path_to_delete.path):
                if path_to_delete.is_dir:
                    shutil.rmtree(path_to_delete.path)
                else:
                    os.remove(path_to_delete.path)
                tree.refresh_path()

    def action_close_right_screen(self) -> None:
        right_display = self.query_one("#right")
        right_tree = right_display.query("DirectoryDisplay")
        if right_tree:
            right_tree[0].remove()
