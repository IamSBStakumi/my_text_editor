import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from functions import file_controller


class PathTreeFrame(ttk.Frame):
    def __init__(self, master=None, path=os.curdir, **kwargs):
        super().__init__(master, **kwargs)
        self.root_path = os.path.abspath(path)
        self.nodes = {}
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self)
        y_scroll_bar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        x_scroll_bar = ttk.Scrollbar(
            self, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=y_scroll_bar, xscrollcommand=x_scroll_bar)

        self.insert_node("", os.path.basename(self.root_path), self.root_path)

        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        y_scroll_bar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        x_scroll_bar.grid(row=1, column=0, sticky=(tk.E, tk.W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="新規ファイル", command=self.create_file)
        self.context_menu.add_command(label="新規フォルダ", command=self.create_folder)

        self.tree.bind("<<TreeviewOpen>>", self.open_node)
        self.tree.bind("<Double-1>", self.choose_file)
        self.tree.bind("<Button-3>", self.popup_context_menu)
        self.bind_all("<Button-1>", self.hide_context_menu_global, add="+")

    def insert_node(self, parent, text, abspath):
        node_label = os.path.basename(abspath) or abspath
        node = self.tree.insert(parent, "end", text=node_label, open=False)

        if os.path.isdir(abspath):
            self.tree.insert(node, "end")
            self.nodes[node] = (False, abspath)
        else:
            self.nodes[node] = (True, abspath)

    def open_node(self, event=None, node=None):
        if node is None:
            node = self.tree.focus()

        already_open, abspath = self.nodes.get(node, (None, None))

        if not already_open:
            self.tree.delete(self.tree.get_children(node))

            for entry in sorted(
                os.scandir(abspath), key=lambda path: path.name.lower()
            ):
                self.insert_node(node, entry.name, os.path.join(abspath, entry.path))

            self.nodes[node] = (True, abspath)

    def choose_file(self, event):
        node = self.tree.focus()

        if node:
            already_open, abspath = self.nodes[node]
            if os.path.isfile(abspath):
                file_controller.event.open_file(file_path=abspath)

    def update_dir(self, event=None):
        self.create_widgets()

    def change_dir(self, event=None):
        dir_name = filedialog.askdirectory()
        if dir_name:
            self.root_path = dir_name
            self.create_widgets()

    def popup_context_menu(self, event):
        node = self.tree.identify_row(event.y)

        if node:
            self.tree.selection_set(node)
            self.context_menu.post(event.x_root, event.y_root)
            self._right_clicked_node = node

    def create_file(self):
        self._create_new_entry(is_folder=False)

    def create_folder(self):
        self._create_new_entry(is_folder=True)

    def _create_new_entry(self, is_folder):
        node = getattr(self, "_right_clicked_node", None)
        if not node:
            return

        _, parent_path = self.nodes.get(node, (None, None))
        if not parent_path:
            return

        name = tk.simpledialog.askstring("名前を入力", "名前を入力してください: ")
        if not name:
            return

        new_path = os.path.join(parent_path, name)

        try:
            if is_folder:
                os.makedirs(new_path)

            else:
                with open(new_path, "w", encoding="utf-8") as f:
                    f.write("")

            self.tree.delete(*self.tree.get_children(node))
            # self.nodes[node] = (False, parent_path)
            self.open_node(node=node)

        except Exception as e:
            tk.messagebox.showerror("エラー", f"作成できませんでした: \n{e}")

    def hide_context_menu_global(self, event=None):
        self.after(100, self._safe_unpost_menu)

    def _safe_unpost_menu(self):
        if hasattr(self, "context_menu"):
            try:
                self.context_menu.unpost()
            except Exception:
                pass
