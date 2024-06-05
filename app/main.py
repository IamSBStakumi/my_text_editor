import tkinter as tk
import tkinter.ttk as ttk

import functions.app_controller as app_controller
import functions.file_controller as file_controller
from frames.editor_tab import EditorTab
from frames.menu import EditorMenu
from frames.path_tree import PathTreeFrame


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.create_file_controller()
        self.create_app_controller()
        self.create_global_shortcuts()

    def create_widgets(self):
        self.path_frame = PathTreeFrame(self)
        self.editor_frame = EditorTab(self)

        self.path_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.editor_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.columnconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(1, weight=3, uniform="group1")
        self.rowconfigure(0, weight=4, uniform="group2")
        self.rowconfigure(0, weight=1, uniform="group2")

    def create_file_controller(self):
        file_controller.set_file_controller(self, self.editor_frame, self.path_frame)

    def create_app_controller(self):
        app_controller.set_app_controller(self, self.master, self.editor_frame)

    def create_global_shortcuts(self):
        self.master.bind("<Control-KeyPress-s>", file_controller.event.save_file)
        self.master.bind("<Control-KeyPress-n>", file_controller.event.new_file)
        self.master.bind("<Control-KeyPress-o>", file_controller.event.open_file)
        self.master.bind("<Control-KeyPress-q>", app_controller.event.quit_app)


def main():
    root = tk.Tk()
    root.title("My Editor")
    app = App(root)
    root["menu"] = EditorMenu()
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()


if __name__ == "__main__":
    main()
