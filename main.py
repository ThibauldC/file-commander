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
        ("q", "quit", "Quit")
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
            left_tree: DirectoryDisplay = self.query_one("#left_tree")
            right_tree: DirectoryDisplay = self.query_one("#right_tree")
            shutil.move(left_tree.get_path().path, right_tree.get_path().path)
            left_tree.refresh_path()
            right_tree.refresh_path()
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
        tree: DirectoryDisplay = e.sender.origin
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


if __name__ == "__main__":
    file_commander = FileCommander()
    file_commander.run()
