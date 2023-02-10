import os
import shutil

from textual.app import App, ComposeResult
from textual.css.query import NoMatches
from textual.widgets import Header, Footer

from src.custom_input import CustomInput
from src.directory_display import DisplayContainer, RightDirectoryDisplay, LeftDirectoryDisplay, DirectoryDisplay, Change


class FileCommander(App):
    CSS_PATH = "../test.css"

    BINDINGS = [
        ("q", "quit", "Quit")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DisplayContainer()
        yield CustomInput()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#left_tree").focus()

    def on_right_directory_display_move(self, m: RightDirectoryDisplay.Move):
        m.stop()
        try:
            left_tree: DirectoryDisplay = self.query_one("#left_tree")
            right_tree: DirectoryDisplay = self.query_one("#right_tree")
            shutil.move(left_tree.get_current_node_entry().path, right_tree.get_current_node_entry().path)
            left_tree.refresh_path()
            right_tree.refresh_path()
        except NoMatches:
            pass

    def on_directory_display_change_event(self, e: DirectoryDisplay.ChangeEvent) -> None:
        e.stop()
        input = self.query_one("CustomInput")
        input.action_to_perform = e.event
        input.origin = e.sender
        input.focus()
        path_to_display = str(e.sender.path)
        if e.event == Change.Rename:
            path_to_display = e.sender.get_current_node_entry().path
        input.value = path_to_display

    @staticmethod
    def on_custom_input_refresh_path(e: CustomInput.RefreshPath):
        e.stop()
        tree = e.sender.origin
        tree.refresh_path()
        e.sender.value = ""
        tree.focus()

    def on_custom_input_change_path(self, e: CustomInput.ChangePath):
        e.stop()
        tree: DirectoryDisplay = e.sender.origin
        new_path = e.sender.value
        if os.path.exists(new_path) and os.path.isdir(new_path):
            tree.remove()
            if isinstance(tree, LeftDirectoryDisplay):
                new_display = LeftDirectoryDisplay(new_path, id=tree.id)
                dom_node_id = "#left"
            elif isinstance(tree, RightDirectoryDisplay):
                new_display = RightDirectoryDisplay(new_path, id=tree.id)
                dom_node_id = "#right"
            else:
                raise Exception("Wrongly submitted input")
            self.query_one(dom_node_id).mount(new_display)
            new_display.focus()
            e.sender.value = ""


def main():
    file_commander = FileCommander()
    file_commander.run()
