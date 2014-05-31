'''
проверка алгоритма взаимодействия с listbox
'''
from tkinter import Tk, Listbox, Scrollbar
from tkinter import END, VERTICAL, RIGHT, LEFT, BOTH, Y

root = Tk()

scrollbar = Scrollbar(root, orient=VERTICAL) #нужен для отображения длинных списков
lb = Listbox(root, yscrollcommand=scrollbar.set) #синхронизируем
scrollbar.config(command=lb.yview)

scrollbar.pack(side=RIGHT, fill=Y)
lb.pack(side=LEFT, fill=BOTH, expand=1)

#Заполняем список
lb.insert(END, "a list entry") #в программе нужно использовать не пустой список, иначе, при выборе элемента программа будет падать. Возможно, есть смысл использовать ключевое слово ALL или None. ALL - покрасить все, None - убрать выбор

for item in ["one", "two", "three", "four","five","six","seven","eight","nine","ten"]:
    lb.insert(END, item)



# for i in dir(lb):
    # if i[0]!='_':
        # print(i)
# root.bind("<Button-1>", lambda event: lb.delete(END))

#выдаем выбранный элемент списка
lb.bind("<<ListboxSelect>>", lambda event: print(lb.get(lb.curselection())))

root.mainloop()