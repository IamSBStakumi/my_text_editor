import tkinter as tk
import tkinter.ttk as ttk

from functions import file_controller


class EditorFrame(ttk.Frame):
    def __init__(self, master, path=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.create_widgets()
        self.create_event()
        self.path = path
        self.changed = False
        self.change_count = 0

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, opening_file_path):
        self._path = opening_file_path

    def create_widgets(self):
        self.text = tk.Text(self, width=80, height=30)
        self.line_numbers = tk.Canvas(self, width=40)
        self.scroll_bar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview
        )

        self.text.configure(yscrollcommand=self.scroll_bar.set)

        self.line_numbers.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.text.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.scroll_bar.grid(row=0, column=2, sticky=(tk.N, tk.S))

        # 縦と、コード入力欄のみ拡大されるよう指定
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def create_event(self):
        self.text.bind("<<Scroll>>", self.on_scroll)

        # TODO: ショートカットキーの入力も捉えてしまう
        self.text.bind("<KeyRelease>", self.on_change)

        # self.text.bind("<Tab>", self.tab)

        # self.text.bind("<BackSpace>", self.back_space)

        self.text.bind("<Configure>", self.update_line_number)

        self.text.bind("<Control-a>", self.select_all)

    def on_scroll(self, event=None):
        self.update_line_number(event=event)

    def on_change(self, event=None):
        self.update_line_number(event=event)

        if self.change_count:
            self.changed = True
            file_controller.event.change_tab_name(event=event)
        self.change_count += 1

    def update_line_number(self, event=None):
        self.line_numbers.delete(tk.ALL)

        first_row = self.text.index("@0,0")
        first_row_number = int(first_row.split(".")[0])

        last_row = self.text.index("end")
        last_row_number = int(last_row.split(".")[0])

        for row_number in range(first_row_number, last_row_number):
            dline = self.text.dlineinfo("{0}.0".format(row_number))

            if dline is None:
                break
            else:
                y = dline[1]

            self.line_numbers.create_text(3, y, anchor=tk.NW, text=row_number, font=14)

    def select_all(self, event=None):
        self.text.tag_add("sel", "1.0", "end")
        return "break"

    def get_src(self):
        return self.text.get("1.0", "end-1c")
