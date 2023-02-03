import os
import shutil

from textual import events
from textual.app import App, ComposeResult
from textual.css.query import NoMatches
from textual.message import Message, MessageTarget
from textual.reactive import reactive, Reactive
from textual.widgets import Header, Footer, Input, TreeNode

from directory_display import DisplayContainer, RightDirectoryDisplay


#TODO: use input to change path
# TODO: use events and/or separate widget classes to clean up code?

class CustomInput(Input):

    class Move(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    # def key_enter(self):
    #     match self.value:
    #         case "move":
    #             self.emit_no_wait(self.Move(self))


class FileCommander(App):
    CSS_PATH = "test.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "test_path", "Test path")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DisplayContainer()
        yield CustomInput(id="text_input")
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.query_one("#left_tree").focus()

    # TODO: make refresh method
    def on_right_directory_display_move(self, m: RightDirectoryDisplay.Move):
        m.stop()
        try:
            left_path = self.query_one("#left_tree").get_path()
            right_path = self.query_one("#right_tree").get_path()
            shutil.move(left_path.path, right_path.path)
        except NoMatches:
            pass

    # def on_input_submitted(self, e: Input.Submitted):
    #     e.stop()
    #     try:
    #         left_path = self.query_one("#left_tree").get_path()
    #         right_path = self.query_one("#right_tree").get_path()
    #         self.query_one("CustomInput").value = f"{left_path} -> {right_path}"
    #     except NoMatches:
    #         pass

    def key_colon(self):
        self.query_one("CustomInput").focus()

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


if __name__ == "__main__":
    file_commander = FileCommander()
    file_commander.run()
