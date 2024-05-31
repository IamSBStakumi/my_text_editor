import tkinter as tk


class EditorMenu(tk.Menu):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.create_file_menu()
        self.create_edit_menu()

    def create_file_menu(self):
        menu_file = tk.Menu(self)
        menu_file.add_command(label="新しいテキストファイル", accelerator="Ctrl+N")
        menu_file.add_separator()
        menu_file.add_command(label="ファイルを開く", accelerator="Ctrl+O")
        menu_file.add_separator()
        menu_file.add_command(label="保存", accelerator="Ctrl+S")
        menu_file.add_command(label="名前を付けて保存", accelerator="Ctrl+Shift+S")
        menu_file.add_separator()
        menu_file.add_command(label="終了", accelerator="Ctrl+Q")
        self.add_cascade(menu=menu_file, label="ファイル")

    def create_edit_menu(self):
        menu_edit = tk.Menu(self)
        menu_edit.add_command(label="検索", accelerator="Ctrl+F")
        menu_edit.add_command(label="置換", accelerator="Ctrl+H")
        self.add_cascade(menu=menu_edit, label="編集")
