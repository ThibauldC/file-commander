import os
import shutil

from textual import events
from textual.app import App, ComposeResult
from textual.css.query import NoMatches
from textual.message import Message, MessageTarget
from textual.widgets import Header, Footer, Input

from directory_display import DisplayContainer, RightDirectoryDisplay, LeftDirectoryDisplay, DirectoryDisplay


class CustomInput(Input):

    def __init__(self, origin: DirectoryDisplay | None = None):
        self.origin = origin
        super().__init__()

    class ChangePath(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)


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
        e.stop()
        tree = e.sender.origin
        if os.path.exists(e.value) and os.path.isdir(e.value):
            tree.remove()
            if isinstance(tree, LeftDirectoryDisplay):
                new_display = LeftDirectoryDisplay(e.value, id=tree.id)
                self.query_one("#left").mount(new_display)
            elif isinstance(tree, RightDirectoryDisplay):
                new_display = RightDirectoryDisplay(e.value, id=tree.id)
                self.query_one("#right").mount(new_display)
            else:
                raise Exception("Wrongly submitted input")
            new_display.focus()
            e.sender.value = ""

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
