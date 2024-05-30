import tkinter
import tkinter.filedialog

def load_text():
    type = [("Text", "*.txt"), ("Python", "*.py")]
    file_name = tkinter.filedialog.askopenfilename(filetypes=type)
    if file_name != "":
        file = None
        try:
            file = open(file_name, "r", encoding="utf-8")
            text_editor.delete("1.0", "end")
            text_editor.insert("1.0", file.read())
        except:
            file = open(file_name, "r", encoding="shift-jis")
            text_editor.delete("1.0", "end")
            text_editor.insert("1.0", file.read())
        finally:
            if file != None:
                file.close()

def save_text():
    type = [("Text", "*.txt")]
    file_name = tkinter.filedialog.asksaveasfilename(filetypes=type)
    if file_name != "":
        if file_name[-4:] != ".txt":
            file_name = file_name + ".txt"
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write(text_editor.get("1.0","end-1c"))

# メイン画面
root = tkinter.Tk()
root.title("テキストエディター")
frame = tkinter.Frame()
frame.pack()
text_editor=tkinter.Text(frame, width=80, height=30)
scroll_bar = tkinter.Scrollbar(frame, orient = tkinter.VERTICAL, command=text_editor.yview)
scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
text_editor.pack()
text_editor[ "yscrollcommand" ] = scroll_bar.set

# メニューバー
menu_bar = tkinter.Menu()
menu_command = tkinter.Menu(menu_bar, tearoff = 0)
menu_command.add_command(label="読み込み", command=load_text)
menu_command.add_separator()
menu_command.add_command(label="書き込み", command=save_text)
menu_bar.add_cascade(label="ファイル", menu=menu_command)
root["menu"] = menu_bar

root.mainloop()