import os
import shutil

from textual import events
from textual.app import App, ComposeResult
from textual.css.query import NoMatches
from textual.message import Message, MessageTarget
from textual.reactive import reactive, Reactive
from textual.widgets import Header, Footer, Input, TreeNode, DirectoryTree

from directory_display import DisplayContainer, RightDirectoryDisplay, LeftDirectoryDisplay, DirectoryDisplay


#TODO: use input to change path
# TODO: use events and/or separate widget classes to clean up code?

class CustomInput(Input):

    def __init__(self, origin: DirectoryDisplay | None = None):
        self.origin = origin
        super().__init__()

    class ChangePath(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    # def key_enter(self):
    #     self.emit_no_wait(self.ChangePath(self))


class FileCommander(App):
    CSS_PATH = "test.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "test_path", "Test path")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DisplayContainer()
        yield CustomInput()
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.query_one("#left_tree").focus()

    def on_right_directory_display_move(self, m: RightDirectoryDisplay.Move):
        m.stop()
        try:
            left_tree = self.query_one("#left_tree")
            right_tree = self.query_one("#right_tree")
            shutil.move(left_tree.get_path().path, right_tree.get_path().path)
            left_tree.clear()
            left_tree.data = left_tree.load_directory(left_tree.root) # TODO: refactor this into refresh method
            #line = right_tree.cursor_line
            right_tree.clear()
            right_tree.data = right_tree.load_directory(right_tree.root) #TODO: but auto-expand tree node that was open? -> cursor_node.label
        except NoMatches:
            pass

    def on_directory_display_change_path(self, e: DirectoryDisplay.ChangePath):
        e.stop()
        input = self.query_one("CustomInput")
        input.origin = e.sender
        input.focus()
        input.value = str(e.sender.path)

    def on_input_submitted(self, e: Input.Submitted):
        e.stop() #BUG: when executed twice in a row it fails
        tree = e.sender.origin
        tree.remove()
        if isinstance(tree, LeftDirectoryDisplay):
            self.query_one("#left").mount(LeftDirectoryDisplay(e.value, id=tree.id))
        elif isinstance(tree, RightDirectoryDisplay):
            self.query_one("#right").mount(RightDirectoryDisplay(e.value, id=tree.id))

    def key_colon(self):
        self.query_one("CustomInput").focus()

    def action_test_path(self) -> None:
        tree = self.query_one("#left_tree")
        try:
            #line = tree._tree_lines[tree.cursor_line]
            line = tree.cursor_node.label.text
        except IndexError:
            pass
        else:
            # node = line.path[-1]
            # dir_entry = node.data
            input = self.query_one("Input")
            input.focus()
            input.value = line


if __name__ == "__main__":
    file_commander = FileCommander()
    file_commander.run()
