import os
import shutil
from pathlib import Path

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var, reactive, Reactive
from textual.widgets import Header, Footer, DirectoryTree, TextLog, Input, TreeNode

#TODO: use input to change path
# TODO: use events and/or separate widget classes to clean up code?
class DirectoryDisplay(DirectoryTree):
    BINDINGS = [
        ("z", "test_binding", "Test Binding")
    ]

    def action_test_binding(self):
        self.reset_focus()


class FileCommander(App):
    CSS_PATH = "test.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("m", "move_file", "Move"),
        ("t", "test_path", "Test path"),
        ("c", "close_right_screen", "Close right screen")
        #add change directory path textlog widget -> set active through focus -> on_key event
    ]
    path: Reactive[str] = reactive("/Users/thibauld.croonenborghs/Desktop/test")
    l_file_path: Reactive[TreeNode[os.DirEntry] | None] = None
    r_file_path: Reactive[TreeNode[os.DirEntry] | None] = None

    def compose(self) -> ComposeResult:
        yield Header()
        #yield Container(DirectoryTree(self.path, id="left"))
        yield Container(Container(DirectoryDisplay(self.path, id="left_tree"), classes="display_container", id="left"), Container(classes="display_container", id="right"), id="test_container")
        yield Input(id="text_input")
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.query_one("#left_tree").focus()

    # def on_directory_tree_file_selected(
    #     self, event: DirectoryTree.FileSelected
    # ) -> None:
    #     """Called when the user click a file in the directory tree."""
    #     event.stop()
    #     self.path = event.path

    # TODO: refactor into separate class?
    def action_move_file(self) -> None:
        left_tree = self.query_one("#left_tree")
        if left_tree.has_focus:
            #does not have to be mounted with second round of moving
            self.query_one("#right").mount(DirectoryDisplay(str(Path.home()), id="right_tree"))
            left_tree.reset_focus()
            self.query_one("#right_tree").focus()
            self.l_file_path = self._get_path("left_tree")
        elif self.query_one("#right_tree").has_focus:
            self.r_file_path = self._get_path("right_tree")
            shutil.move(self.l_file_path.data.path, self.r_file_path.data.path)
            left_tree.remove()
            self.query_one("#right_tree").remove()
            self.query_one("#left").mount(DirectoryDisplay(self.path, id="left_tree"))
            self.query_one("#right").mount(DirectoryDisplay(self.r_file_path.data.path, id="right_tree"))
            self.query_one("#left_tree").focus()
        else:
            pass

    def action_close_right_screen(self) -> None:
        self.query_one("#right_tree").remove()

    def action_test_path(self) -> None:
        tree = self.query_one("#left_tree")
        try:
            line = tree._tree_lines[tree.cursor_line]
        except IndexError:
            pass
        else:
            node = line.path[-1]
            dir_entry = node.data
            input = self.query_one("Input")
            input.focus()
            input.value = dir_entry.path

    def _get_path(self, tree_id: str) -> TreeNode[os.DirEntry]:
        tree = self.query_one(f"#{tree_id}")
        line = tree._tree_lines[tree.cursor_line]
        node = line.path[-1]
        return node


if __name__ == "__main__":
    file_commander = FileCommander()
    file_commander.run()
