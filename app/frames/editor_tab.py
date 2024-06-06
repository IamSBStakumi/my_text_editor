import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

from frames.editor import EditorFrame


class EditorTab(ttk.Notebook):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        f = open("./app/images/delete.png", "rb")
        photo_data = f.read()
        f.close()
        self.delete_button = tk.PhotoImage(data=photo_data)

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

        self.add(editor, text=name, image=self.delete_button, compound="right")

        now_open_tab = self.tabs()[-1]
        self.select(now_open_tab)
        editor.text.focus_set()
        return "break"

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

    def delete_tab(self, event=None, editor=None):
        if editor.changed:
            if messagebox.askyesno(
                message="変更した内容は保存されませんが、よろしいですか"
            ):
                self._delete_current_tab()

        else:
            self._delete_current_tab()

    def get_current_editor(self):
        current_widget_name = self.select().split(".")[-1]
        text_widget = self.children[current_widget_name]
        return text_widget

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

    def change_tab_name(self, event=None):
        current_tab = self.select()
        tab_name = self.tab(current_tab)["text"].replace("*", "")
        self.tab(current_tab, text="*" + tab_name)

    def reset_tab_name(self, event=None):
        current_tab = self.select()
        tab_name = self.tab(current_tab)["text"].replace("*", "")
        self.tab(current_tab, text=tab_name)
