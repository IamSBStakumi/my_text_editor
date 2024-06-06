import tkinter as tk


class TreeMenu(tk.Entry):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.is_display = False

    def create_widgets(self):
        # treeを操作するメニュー
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="新しいファイル")
        self.menu.add_command(label="新しいフォルダ")
        self.menu.add_separator()
        # 任意の箇所をクリックするだけでメニューを閉じれるようにしたい
        self.menu.add_command(label="閉じる")

    def show_menu(self, event=None):
        try:
            self.menu.tk_popup(event.x_root, event.y_root, not bool(self.is_display))
            self.is_display = not bool(self.is_display)
        finally:
            self.menu.grab_release()
            self.is_display = not bool(self.is_display)
