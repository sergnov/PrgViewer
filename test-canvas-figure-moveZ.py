from tkinter import Tk, Canvas

def ev(func,mess="Hello"):
    print(mess)
    func()

root = Tk()
c = Canvas(root,width=500,height=500,bg="white")
c.create_rectangle(208,208,252,252,outline="red",fill="red",tag="FIG")
c.create_text(252,208,anchor="nw",text="FIG",fill="red",tag="FIG")
c.create_rectangle(220,220,304,304,outline="black",fill="black",tag="DESC")
c.create_text(304,220,anchor="nw",text="DESC",fill="black",tag="DESC")

root.bind("<Key-u>", lambda event:ev(lambda: c.tag_raise("DESC"),mess="DESC-UP"))####
root.bind("<Key-d>", lambda event:ev(lambda: c.tag_lower("DESC"),mess="DESC-DOWN"))####
root.bind("<Key-U>", lambda event:ev(lambda: c.tag_raise("FIG"), mess="FIG-UP"))####
root.bind("<Key-D>", lambda event:ev(lambda: c.tag_lower("FIG"), mess="FIG-DOWN"))####

root.bind("<Key-Up>",         lambda event:c.move("FIG",5,5))
root.bind("<Key-Down>",       lambda event:c.move("FIG",-5,-5))
root.bind("<Shift-Key-Up>",   lambda event:c.move("DESC",5,5))
root.bind("<Shift-Key-Down>", lambda event:c.move("DESC",-5,-5))

c.pack()
root.mainloop()