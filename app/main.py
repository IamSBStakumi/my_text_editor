import tkinter as tk
import tkinter.ttk as ttk

from frames.editor import EditorFrame
from frames.menu import EditorMenu

# import tkinter.filedialog

# app_name = "テキストエディター"

# def load_text(self, event=None):
#     type = [("Markdown", "*.md"), ("Text", "*.txt"), ("Python", "*.py")]
#     file_name = tkinter.filedialog.askopenfilename(filetypes=type)
#     if file_name != "":
#         file = None
#         try:
#             file = open(file_name, "r", encoding="utf-8")
#             self.text_editor.delete("1.0", "end")
#             self.text_editor.insert("1.0", file.read())
#         except:
#             file = open(file_name, "r", encoding="shift-jis")
#             self.text_editor.delete("1.0", "end")
#             self.text_editor.insert("1.0", file.read())
#         finally:
#             if file != None:
#                 file.close()


# def create_new_file():
#     file_name = tkinter.filedialog.asksaveasfilename(
#         title="名前を付けて保存",
#         filetypes = [("Markdown", "*.md"), ("Text", "*.txt"), ("Python", "*.py")],
#         initialdir="./"
#     )
#     if file_name != "":
#         with open(file_name, 'w', encoding="utf-8") as file:
#             file.write(text_editor.get("1.0","end-1c"))

# def save_text():
#     type = [(("Markdown", "*.md"))]
#     file_name = tkinter.filedialog.asksaveasfilename(filetypes=type)
#     if file_name != "":
#         if file_name[-3:] != ".md":
#             file_name = file_name + ".md"
#         with open(file_name, 'w', encoding="utf-8") as file:
#             file.write(text_editor.get("1.0","end-1c"))

# def quit_app():
#     root.destroy()

# # メイン画面
# root = tkinter.Tk()
# root.title(app_name)
# frame = tkinter.Frame()
# frame.pack()
# text_editor=tkinter.Text(frame, width=80, height=30)
# scroll_bar = tkinter.Scrollbar(frame, orient = tkinter.VERTICAL, command=text_editor.yview)
# scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# text_editor.pack()
# text_editor[ "yscrollcommand" ] = scroll_bar.set


# # メニューバー
# menu_bar = tkinter.Menu()
# menu_command = tkinter.Menu(menu_bar, tearoff = 0)
# menu_command.add_command(label="新しいテキストファイル", command=create_new_file, accelerator="Ctrl+N")
# root.bind("<Control-Key-n>", create_new_file)
# menu_command.add_command(label="読み込み", command=fc.load_text(text_editor), accelerator="Ctrl+O")
# root.bind("<Control-Key-o>", fc.load_text(text_editor))
# menu_command.add_separator()
# menu_command.add_command(label="書き込み", command=save_text, accelerator="Ctrl+S")
# root.bind("<Control-Key-s>", save_text)
# menu_command.add_separator()
# menu_command.add_command(label="終了", command=quit_app, accelerator="Ctrl+Q")
# root.bind("<Control-Key-q>", quit_app)

# menu_bar.add_cascade(label="ファイル", menu=menu_command)

# root["menu"] = menu_bar

# root.mainloop()


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

        # text_editor = tkinter.Text(self, width=80, height=30)
        # scroll_bar = tkinter.Scrollbar(
        #     self, orient=tkinter.VERTICAL, command=text_editor.yview
        # )
        # scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # text_editor.pack()
        # text_editor["yscrollcommand"] = scroll_bar.set

        # self.create_menu_bar()

    def create_widgets(self):
        self.editor_frame = EditorFrame(self)

        self.editor_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    # def create_menu_bar(self):
    #     menu_bar = tk.Menu(self)
    #     menu_command = tk.Menu(menu_bar, tearoff=0)
    #     menu_command.add_command(
    #         label="新しいテキストファイル", command=self.load_file, accelerator="Ctrl+N"
    #     )
    #     menu_command.add_command(
    #         label="終了", command=self.quit_app, accelerator="Ctrl+Q"
    #     )
    #     menu_bar.add_cascade(label="ファイル", menu=menu_command)

    #     self.master.config(menu=menu_bar)

    # def load_file(self, event=None):
    #     load_text(self)

    # def quit_app(self, event=None):
    #     self.master.destroy()


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
