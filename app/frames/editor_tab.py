import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from editor import EditorFrame

class EditorTab(ttk.Notebook):
    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)

    def add_tab(self, event=None, path=None):
        editor = EditorFrame(self, path)

        if(path is None):
            name = "new file"

            editor.change_count += 1

        else:
            name = os.path.basename(path)
            with open(path, "r", encoding="utf-8") as file:
                editor.text.insert("1.0", file.read())

        self.add(editor, text=name)

        now_open_tab = self.tabs()[-1]
        self.select(now_open_tab)
        return "break"
    
    def save_file(self, event=None, initial_dir=os.curdir):
        if not self.tabs():
            return "break"
        
        current_editor = self.get_current_editor()
        src = current_editor.get_src()

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