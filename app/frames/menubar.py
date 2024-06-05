import tkinter as tk

from functions import app_controller, file_controller


class EditorMenubar(tk.Menu):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.create_file_menu()
        # self.create_edit_menu()

    def create_file_menu(self):
        menu_file = tk.Menu(self)
        menu_file.add_command(
            label="新しいテキストファイル",
            command=file_controller.event.new_file,
            accelerator="Ctrl+N",
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="ファイルを開く",
            command=file_controller.event.open_file,
            accelerator="Ctrl+O",
        )
        menu_file.add_command(
            label="フォルダを開く",
            command=file_controller.event.change_dir,
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="保存", command=file_controller.event.save_file, accelerator="Ctrl+S"
        )
        menu_file.add_command(
            label="名前を付けて保存",
            command=file_controller.event.save_as,
            accelerator="Ctrl+Shift+S",
        )
        menu_file.add_separator()
        menu_file.add_command(
            label="終了", command=app_controller.event.quit_app, accelerator="Ctrl+Q"
        )
        self.add_cascade(menu=menu_file, label="ファイル")

    # def create_edit_menu(self):
    #     menu_edit = tk.Menu(self)
    #     menu_edit.add_command(label="検索", accelerator="Ctrl+F")
    #     menu_edit.add_command(label="置換", accelerator="Ctrl+H")
    #     self.add_cascade(menu=menu_edit, label="編集")
