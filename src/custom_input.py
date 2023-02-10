import os
import shutil

from textual.message import Message, MessageTarget
from textual.widgets import Input

from src.directory_display import DirectoryDisplay, Change


class CustomInput(Input):

    def __init__(self, origin: DirectoryDisplay | None = None, action_to_perform: str | Change | None = None):
        self.origin = origin
        self.action_to_perform = action_to_perform
        super().__init__()

    class ChangePath(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    class RefreshPath(Message):
        def __init__(self, sender: MessageTarget):
            super().__init__(sender)

    async def action_submit(self) -> None:
        match self.action_to_perform:
            case Change.NewFile:
                if not os.path.exists(self.value):
                    with open(self.value, "w"):
                        pass
                self.emit_no_wait(self.RefreshPath(self))
            case Change.NewDir:
                if not os.path.exists(self.value):
                    os.mkdir(self.value)
                self.emit_no_wait(self.RefreshPath(self))
            case Change.ChangePath:
                self.emit_no_wait(self.ChangePath(self))
            case Change.Rename:
                os.rename(self.origin.get_current_node_entry().path, self.value)
                self.emit_no_wait(self.RefreshPath(self))
            case Change.Delete:
                entry_to_delete = self.origin.get_current_node_entry()
                if os.path.exists(entry_to_delete.path):
                    if entry_to_delete.is_dir:
                        shutil.rmtree(entry_to_delete.path)
                    else:
                        os.remove(entry_to_delete.path)
                self.emit_no_wait(self.RefreshPath(self))
            case _:
                self.value = "this doesn't work"
