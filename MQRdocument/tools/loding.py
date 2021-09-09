import tkinter 

root = tkinter.Tk()
photo = tkinter.PhotoImage(file="C:/MQRdocument/tools/testload.gif")
gif_index = 0

def next_frame():
    global gif_index
    try:
        # XXX: 次のフレームに移る
        photo.configure(format="gif -index {}".format(gif_index))

        gif_index += 1
    except tkinter.TclError:
        gif_index = 0
        return next_frame()
    else:
        root.after(100, next_frame) # XXX: アニメーション速度が固定

label = tkinter.Label(root, image=photo)
label.pack()

root.after_idle(next_frame)
root.mainloop()