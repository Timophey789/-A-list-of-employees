import tkinter as tk#Импортируем нужные библиотеки
from tkinter import ttk
import sqlite3


class Main(tk.Frame):#Создаем класс в котором будем прописывать основную логику приложения
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):#Создаем калсс через еоторыей будет осуществляться добавление нового сотрудника
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d8e0", bd=0, image=self.add_img, command=self.open_dialog
        )
        btn_open_dialog.pack(side=tk.LEFT)#Распологаем кнопку

        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email","salary"), height=45, show="headings"
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)#Создаем колонки которые будет заполнять пользователь и располагаем их.
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file="./img/update.png")#Добавляем кнопку обнавления информации о сотруднике и располагаем ее
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file="./img/delete.png")#Добавляем кнопку удаления информации о сотруднике и располагаем ее
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_img,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="./img/search.png")#Добавляем кнопку поиска информации о сотруднике и располагаем ее
        btn_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")#Добавляем кнопку обнавления информации о сотруднике и располагаем ее
        btn_refresh = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.refresh_img,
            command=self.open_search_dialog,
        )
        btn_refresh.pack(side=tk.LEFT)

    def open_dialog(self):#Добавляем функционал для кнопки добавления
        Child()

    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    def view_records(self):
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    def open_update_dialog(self):#Добавляем функционал для кнопки обновления
        Update()

    def update_records(self, name, tel, email,salary):
        self.db.cursor.execute(
            """UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?""",
            (name, tel, email,salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self):#Добавляем функционал для кнопки поиска
        Search()

    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()#перехватывает все события которые происходят внутри окна 
        self.focus_set()#захватывает исключительно события связанные с этим окном 

        label_name = tk.Label(self, text="ФИО:")#Добавляем колонки для заполнения пользователем и располагаем их
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text="Зарплата:")
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(#Добавляем кнопки и сохранем написанное пользователем
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(),self.entry_salary.get()
            ),
        )


class Update(Child):#Оформление и функционал для кнопки обновления
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title("Редактирование информацию о сотруднике")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind(
            "<Button-1>",#Добавляем кнопку и сохраняем данные
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(),self.entry_salary.get()
            ),
        )
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

    def default_data(self):#Отображаем написанное используя информацию из базы данных
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0,row[4])


class Search(tk.Toplevel):#Оформляем и добавляем функционал для кнопки поиска
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title("Поиск сотрудника")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)
        search_btn.bind(
            "<Button-1>",#Добавляем кнопку и сохраняем данные
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")#Создаем базу данных с нужными полями
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT,
                salary INT
            )"""
        )
        self.conn.commit()

    def insert_data(self, name, tel, email,salary):
        self.cursor.execute(
            """INSERT INTO db(name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary)
        )
        self.conn.commit()


if __name__ == "__main__":#Создаем окно приложения
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("800x500")
    root.resizable(False, False)
    root.mainloop()
#Приведенный выше код представляет собой простое приложение хранение информации о сотрудниках, созданное с использованием библиотеки Tkinter на Python. Он позволяет пользователю добавлять, редактировать, удалять и искать информацию о сотрудниках в базе данных SQLite. В приложении есть м.
# Окно с панелью инструментов, содержащей кнопки для добавления, редактирования, удаления и поиска информацию о сотрудниках. В главном окне также есть виджет дерева, отображающий информацию о сотрудниках в базе данных.
# Чтобы добавить новую информацию о сотрудниках, пользователь может нажать кнопку «Добавить» на панели инструментов, после чего откроется новое окно с полями ввода имени, номера телефона, электронной почты и зарплаты. Пользователь может ввести контактные данные и нажать кнопку «Добавить», чтобы добавить информацию о сотрудниках в базу данных.
# Чтобы отредактировать существующий контакт, пользователь может выбрать контакт из дерева и нажать кнопку «Редактировать» на панели инструментов. Откроется новое окно с контактными данными, предварительно заполненными в полях ввода. Пользователь может внести изменения и нажать кнопку «Редактировать», чтобы обновить контакт в базе данных.
# Чтобы удалить информацию о сотрудниках, пользователь может выбрать информацию о сотрудниках  и нажать кнопку «Удалить» на панели инструментов. Это удалит информацию о сотрудниках из базы данных.
# Для поиска информацию о сотрудниках пользователь может нажать кнопку «Поиск» на панели инструментов, после чего откроется новое окно с полем ввода для поиска. Пользователь может ввести имя или часть имени и нажать кнопку «Поиск», чтобы найти информацию о сотрудниках, соответствующие поисковому запросу.
# Приложение также имеет кнопку обновления на панели инструментов, которая обновляет  представление последними данными из базы данных.
# В коде используются концепции объектно-ориентированного программирования для создания различных классов для главного окна, дочернего окна, окна обновления и окна поиска. Он также использует операции с базой данных SQLite для хранения и извлечения данных из базы данных.
# В целом, это приложение телефонной книги представляет собой простой, но полезный инструмент для управления контактами, который можно расширить, добавив дополнительные функции и возможности.