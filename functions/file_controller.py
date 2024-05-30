import tkinter

def load_text(text_editor):
    type = [("Markdown", "*.md"), ("Text", "*.txt"), ("Python", "*.py")]
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
