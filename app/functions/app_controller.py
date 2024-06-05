from tkinter import messagebox


class MockFunctions:
    def __getattribute__(self, name):
        def inner(*args, **kwargs):
            print("call", name, args, kwargs)

        return inner


class Functions:
    def __init__(self, main_frame, root, editor_frame):
        self.main_frame = main_frame
        self.editor_frame = editor_frame
        self.root = root

    def quit_app(self, event=None):
        # TODO: ファイルの変更が保存されていなければ、messageboxを出す
        if not self.editor_frame.tabs():
            self.root.destroy()

        editors = self.editor_frame.winfo_children()
        for editor in editors:
            if editor.changed:
                Messagebox = messagebox.askquestion(
                    message="変更した内容は保存されませんが、よろしいですか"
                )
                if Messagebox == "yes":
                    self.root.destroy()
                    break
                else:
                    break
        # self.root.destroy()


event = MockFunctions()


def set_app_controller(*widgets, default_controller_class=Functions):
    event = default_controller_class(*widgets)
    globals()["event"] = event
