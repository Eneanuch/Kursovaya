from tkinter import *
from tkinter import ttk




if __name__ == "__main__":
    root = Tk()
    root.title("Панель управления Raspberry Pi")
    root.geometry("350x100")
    
    btn1 = ttk.Button(text="Включение ПК", command=turn_on)
    btn1.pack()
    btn2 = ttk.Button(text="Выключение ПК", command=click_button2)
    btn2.pack()
    btn3 = ttk.Button(text="Отправка СМС", command=print(1))
    btn3.pack()
    
    root.mainloop()
    