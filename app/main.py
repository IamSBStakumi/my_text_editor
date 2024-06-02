import tkinter as tk
import tkinter.ttk as ttk

import functions.file_controller as file_controller

from frames.editor import EditorFrame
from frames.menu import EditorMenu
from frames.path_tree import PathTreeFrame

class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.create_file_controller()

    def create_widgets(self):
        self.path_frame = PathTreeFrame(self)
        self.editor_frame = EditorFrame(self)

        self.path_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.editor_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))


    def create_file_controller(self):
        file_controller.set_file_controller(
            self, self.editor_frame, self.path_frame
        )

def main():
    root = tk.Tk()
    root.title("My Editor")
    app = App(master=root)
    root["menu"] = EditorMenu()
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app.mainloop()


if __name__ == "__main__":
    main()
