import tkinter as tk
import tkinter.ttk as ttk


class SearchBox(ttk.Frame):
    def __init__(self, master, text_widget, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        # 検索対象となるテキストウィジェット
        self.target_text = text_widget
        self.create_widgets()
        self.last_text = ""
        self.all_pos = []
        self.next_pos_index = 0
        self.text.focus()

    def create_widgets(self):
        self.text_var = tk.StringVar()
        self.text = ttk.Entry(self, textvariable=self.text_var)
        self.text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        self.text.bind("<Return>", self.search)

    def search_start(self, text):
        # 変数の初期化
        self.next_pos_index = 0
        self.all_pos = []

        start_index = "1.0"
        while True:
            pos = self.target_text.search(text, start_index, stopindex="end")
            if not pos:
                break
            self.all_pos.append(pos)
            start_index = "{0}+1c".format(pos)

        self.search_next(text)

    def search_next(self, text):
        try:
            # 今回のマッチ部分の取得を試みる
            pos = self.all_pos[self.next_pos_index]
        except IndexError:
            # all_posが空でなくIndexErrorならば、全てのマッチを見た、ということ
            # なのでnext_post_indexを0にし、最初からまたマッチを見せる
            if self.all_pos:
                self.next_pos_index = 0
                self.search_next(text)
        else:
            # 次のマッチ部分を取得できればここ
            start = pos
            end = "{0} + {1}c".format(pos, len(text))

            # マッチ部分〜マッチ部分+文字数分 の範囲を選択する
            self.target_text.tag_add("sel", start, end)

            # インサートカーソルをマッチした部分に入れ、スクロールもしておく
            self.target_text.mark_set("insert", start)
            self.target_text.see("insert")

            # 次回取得分のために+1
            self.next_pos_index += 1

    def search(self, event=None):
        """文字の検索を行う."""
        # 現在選択中の部分を解除
        self.target_text.tag_remove("sel", "1.0", "end")

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()

        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.last_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            self.search_start(now_text)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text)

        # 今回の入力を、「前回入力文字」にする
        self.last_text = now_text


def create_search_box(text_widget, title="Search Box"):
    window = tk.Toplevel()
    window.title(title)
    box = SearchBox(window, text_widget)
    box.pack()
