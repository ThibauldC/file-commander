import os

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import var
from textual.widgets import Header, Footer, DirectoryTree, TextLog, Input


class FileCommander(App):
    CSS_PATH = "test.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("m", "move_file", "Move")
        #add change directory path textlog widget -> set active through focus -> on_key event
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(DirectoryTree("/Users/thibauld.croonenborghs/Desktop/test", id="left"))
        yield Input(id="text_input")
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.query_one("#left").focus()

    def action_move_file(self) -> None:
        self.query_one("#left").reset_focus()
        self.query_one("Input").focus()


if __name__ == "__main__":
    file_commander = FileCommander()
    file_commander.run()
