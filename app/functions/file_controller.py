from os.path import expanduser
from typing import Any

home_dir = expanduser("~")

class MockFunctions:
    def __getattribute__(self, name):
        def inner(*args, **kwargs):
            print("call", name, args, kwargs)
        return inner
    
class Functions(MockFunctions):
    def __init__(self, main_frame, editor_frame, path_frame):
        self.main_frame = main_frame
        self.editor_frame = editor_frame

    def save_file(self, event=None, initial_dir=None):
        if initial_dir is None:
            pass
        return self.editor_frame.save_file(event=event, initial_dir=initial_dir)
    
    def new_file(self, event=None):
        return self.editor_frame.add_tab(event=event)
    

    def open_file(self, event=None, file_path=None, initial_dir=None):
        if initial_dir is None:
            initial_dir = self.path_frame.root_path
        return self.editor_frame.open_file(
            event=event, file_path=file_path, initial_dir=initial_dir
        )
    
def set_file_controller(*widgets, default_controller_class=Functions):
    event = default_controller_class(*widgets)
    globals()["event"] = event