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
        if not self.editor_frame.tabs():
            self.root.destroy()

        # 上記destroyが呼び出されても、winfo_childrenが呼び出されてしまう
        # その際にコンソールに警告が出るのでelseを追加
        else:
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
                else:
                    self.root.destroy()


event = MockFunctions()


def set_app_controller(*widgets, default_controller_class=Functions):
    event = default_controller_class(*widgets)
    globals()["event"] = event
