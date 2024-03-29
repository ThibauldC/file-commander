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
        message = self.RefreshPath(self)
        match self.action_to_perform:
            case Change.NewFile:
                if not os.path.exists(self.value):
                    with open(self.value, "w"):
                        pass
            case Change.NewDir:
                if not os.path.exists(self.value):
                    os.mkdir(self.value)
            case Change.ChangePath:
                message = self.ChangePath(self)
            case Change.Rename:
                os.rename(self.origin.get_current_node_entry().path, self.value)
            case Change.Delete:
                entry_to_delete = self.origin.get_current_node_entry()
                if os.path.exists(entry_to_delete.path):
                    if entry_to_delete.is_dir:
                        shutil.rmtree(entry_to_delete.path)
                    else:
                        os.remove(entry_to_delete.path)
            case _:
                self.value = "this doesn't work"
        self.post_message_no_wait(message)
