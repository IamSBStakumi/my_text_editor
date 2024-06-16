import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

from frames.editor import EditorFrame


class EditorTab(ttk.Notebook):
    def __init__(self, master=None, **kwargs):
        self.__initialized_custom_style()
        kwargs["style"] = "CustomNotebook"
        super().__init__(master, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    # Style定義
    def __initialized_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage(
                "img_close",
                data="""
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                """,
            ),
            tk.PhotoImage(
                "img_closeactive",
                data="""
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                """,
            ),
            tk.PhotoImage(
                "img_closepressed",
                data="""
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            """,
            ),
        )

        style.element_create(
            "close",
            "image",
            "img_close",
            ("active", "pressed", "!disabled", "img_closepressed"),
            ("active", "!disabled", "img_closeactive"),
            border=8,
            sticky="",
        )

        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout(
            "CustomNotebook.Tab",
            [
                (
                    "CustomNotebook.tab",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "CustomNotebook.padding",
                                {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [
                                        (
                                            "CustomNotebook.label",
                                            {"side": "left", "sticky": ""},
                                        ),
                                        (
                                            "CustomNotebook.close",
                                            {"side": "left", "sticky": ""},
                                        ),
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )

    # -----------------------------
    # タブ操作の関数
    # -----------------------------
    def add_tab(self, event=None, path=None):
        editor = EditorFrame(self, path)

        if path is None:
            name = "*new file"

            editor.change_count += 1
            editor.changed = True

        else:
            name = os.path.basename(path)
            with open(path, "r", encoding="utf-8") as file:
                editor.text.insert("1.0", file.read())

        self.add(editor, text=name)

        now_open_tab = self.tabs()[-1]
        self.select(now_open_tab)
        editor.text.focus_set()
        return "break"

    def _delete_current_tab(self):
        current = self.select()
        self.forget(current)

    def delete_current_tab(self, event=None):
        if not self.tabs():
            return "break"

        current_editor = self.get_current_editor()
        if current_editor.changed:
            if messagebox.askyesno(
                message="変更した内容は保存されませんが、よろしいですか"
            ):
                self._delete_current_tab()

        else:
            self._delete_current_tab()

    def on_close_press(self, event):
        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(["pressed"])
            self._active = index
            return "break"

    def on_close_release(self, event):
        if not self.instate(["pressed"]):
            return

        element = self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            widget_name = self.tabs()[index].split(".")[-1]
            editor = self.children[widget_name]

            if editor.changed:
                if messagebox.askyesno(
                    message="変更した内容は保存されませんが、よろしいですか"
                ):
                    self.forget(index)
                    self.event_generate("<<NotebookTabClosed>>")

            else:
                self.forget(index)
                self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def get_current_editor(self):
        current_widget_name = self.select().split(".")[-1]
        text_widget = self.children[current_widget_name]
        return text_widget

    def change_tab_name(self, event=None):
        current_tab = self.select()
        tab_name = self.tab(current_tab)["text"].replace("*", "")
        self.tab(current_tab, text="*" + tab_name)

    def reset_tab_name(self, event=None):
        current_tab = self.select()
        tab_name = self.tab(current_tab)["text"].replace("*", "")
        self.tab(current_tab, text=tab_name)

    # ---------------------
    # ファイル操作の関数
    # ---------------------
    def open_file(self, event=None, file_path=None, initial_dir=os.curdir):
        if file_path is None:
            file_path = filedialog.askopenfilename(initialdir=initial_dir)

        if file_path:
            for tab in self.tabs():
                widget_name = tab.split(".")[-1]
                editor = self.children[widget_name]
                if editor.path == file_path:
                    self.select(tab)
                    return "break"

            return self.add_tab(path=file_path)

    def save_file(self, event=None, initial_dir=os.curdir):
        if not self.tabs():
            return "break"

        current_editor = self.get_current_editor()
        src = current_editor.get_src()

        if current_editor.path is None:
            file_name = filedialog.asksaveasfilename(initialdir=initial_dir)
            if file_name:
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(src)
                    current_editor.path = file.name
                    self.tab(current_editor, text=os.path.basename(file.name))

        else:
            with open(current_editor.path, "w", encoding="utf-8") as file:
                file.write(src)
                current_editor.changed = False
                self.reset_tab_name()

    def save_as(self, event=None, initial_dir=os.curdir):
        if not self.tabs():
            return "break"

        current_editor = self.get_current_editor()
        src = current_editor.get_src()

        file_name = filedialog.asksaveasfilename(initialdir=initial_dir)
        if file_name:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(src)
                current_editor.changed = False
                self.reset_tab_name()
