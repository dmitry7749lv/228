import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from config import APP_NAME
from models import create_tables
from auth import login_user, register_user
from products import get_products, delete_product, create_product  


class App:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)

        width = 1280
        height = 760

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)

        self.user = None

        self.configure_styles()
        self.show_login()

    def configure_styles(self):
        style = tb.Style()

        style.configure(
            "Treeview",
            rowheight=42,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 11, "bold")
        )

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()

        # Основной контейнер
        container = tb.Frame(self.root, padding=40)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        tb.Label(
            container,
            text=APP_NAME,
            font=("Segoe UI", 30, "bold")
        ).pack(pady=(0, 30))

        tb.Label(
            container,
            text="Авторизация",
            font=("Segoe UI", 14)
        ).pack(pady=(0, 20))

        self.login_entry = tb.Entry(container, width=40)
        self.login_entry.pack(pady=10, ipady=8)
        self.login_entry.focus()

        self.password_entry = tb.Entry(
            container,
            width=40,
            show="*"
        )
        self.password_entry.pack(pady=10, ipady=8)

        # Кнопки в ряд
        button_frame = tb.Frame(container)
        button_frame.pack(pady=20)

        tb.Button(
            button_frame,
            text="Войти",
            bootstyle=PRIMARY,
            width=15,
            command=self.login
        ).pack(side=LEFT, padx=5)

        tb.Button(
            button_frame,
            text="Регистрация",
            bootstyle=SUCCESS,
            width=15,
            command=self.show_register
        ).pack(side=LEFT, padx=5)

        tb.Button(
            button_frame,
            text="Гость",
            bootstyle=SECONDARY,
            width=15,
            command=self.guest_login
        ).pack(side=LEFT, padx=5)

    def show_register(self):
        self.clear()

        container = tb.Frame(self.root, padding=40)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        tb.Label(
            container,
            text="Регистрация",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(0, 25))

        self.name_entry = tb.Entry(container, width=40)
        self.name_entry.pack(pady=10, ipady=8)

        self.login_entry = tb.Entry(container, width=40)
        self.login_entry.pack(pady=10, ipady=8)

        self.password_entry = tb.Entry(
            container,
            width=40,
            show="*"
        )
        self.password_entry.pack(pady=10, ipady=8)

        # Кнопки в ряд
        button_frame = tb.Frame(container)
        button_frame.pack(pady=20)

        tb.Button(
            button_frame,
            text="Создать аккаунт",
            bootstyle=SUCCESS,
            width=18,
            command=self.register
        ).pack(side=LEFT, padx=5)

        tb.Button(
            button_frame,
            text="Назад",
            bootstyle=SECONDARY,
            width=18,
            command=self.show_login
        ).pack(side=LEFT, padx=5)

    def register(self):
        success, message = register_user(
            self.name_entry.get(),
            self.login_entry.get(),
            self.password_entry.get()
        )

        if success:
            messagebox.showinfo(
                "Успех",
                message
            )
            self.show_login()
        else:
            messagebox.showerror(
                "Ошибка",
                message
            )

    def login(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if not login or not password:
            messagebox.showwarning(
                "Ошибка",
                "Введите логин и пароль"
            )
            return

        self.user = login_user(login, password)

        if self.user:
            self.show_products()
        else:
            messagebox.showerror(
                "Ошибка",
                "Неверный логин или пароль"
            )

    def guest_login(self):
        self.user = {"role": "Гость"}
        self.show_products()

    def show_products(self):
        self.clear()

        # Верхняя панель
        header = tb.Frame(self.root, padding=20)
        header.pack(fill=X)

        tb.Label(
            header,
            text=APP_NAME,
            font=("Segoe UI", 24, "bold")
        ).pack(side=LEFT)

        tb.Label(
            header,
            text=f"Роль: {self.user['role']}",
            font=("Segoe UI", 12)
        ).pack(side=RIGHT)

        # Основное содержимое
        content = tb.Frame(self.root, padding=(20, 0))
        content.pack(fill=BOTH, expand=True)

        # Поиск
        search_frame = tb.Frame(content)
        search_frame.pack(fill=X, pady=(0, 15))

        self.search_entry = tb.Entry(
            search_frame,
            font=("Segoe UI", 11)
        )

        self.search_entry.pack(
            side=LEFT,
            fill=X,
            expand=True,
            ipady=8
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_products
        )

        # Таблица
        columns = ("article", "name", "price", "quantity")

        self.tree = tb.Treeview(
            content,
            columns=columns,
            show="headings"
        )

        self.tree.heading("article", text="Артикул")
        self.tree.heading("name", text="Название")
        self.tree.heading("price", text="Цена")
        self.tree.heading("quantity", text="Количество")

        self.tree.column("article", width=180, anchor=CENTER)
        self.tree.column("name", width=620)
        self.tree.column("price", width=180, anchor=CENTER)
        self.tree.column("quantity", width=180, anchor=CENTER)

        self.tree.pack(fill=BOTH, expand=True)

        # Нижняя панель с кнопками
        footer = tb.Frame(self.root, padding=20)
        footer.pack(fill=X)

        # Левая группа кнопок (действия с товарами)
        left_buttons = tb.Frame(footer)
        left_buttons.pack(side=LEFT)

        if self.user["role"] == "Администратор":
            tb.Button(
                left_buttons,
                text="➕ Добавить товар",
                bootstyle=SUCCESS,
                command=self.add_product
            ).pack(side=LEFT, padx=5)

            tb.Button(
                left_buttons,
                text="🗑️ Удалить товар",
                bootstyle=DANGER,
                command=self.delete_selected
            ).pack(side=LEFT, padx=5)

        # Правая группа кнопок (навигация)
        right_buttons = tb.Frame(footer)
        right_buttons.pack(side=RIGHT)

        tb.Button(
            right_buttons,
            text="🔄 Обновить",
            bootstyle=INFO,
            command=lambda: self.load_products(self.search_entry.get())
        ).pack(side=LEFT, padx=5)

        tb.Button(
            right_buttons,
            text="🚪 Выход",
            bootstyle=SECONDARY,
            command=self.show_login
        ).pack(side=LEFT, padx=5)

        self.load_products()

    def load_products(self, search=""):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for product in get_products(search):
            self.tree.insert(
                "",
                END,
                iid=product["id"],
                values=(
                    product["article"],
                    product["name"],
                    f"{product['price']} ₽",
                    product["quantity"]
                )
            )

    def search_products(self, event=None):
        self.load_products(self.search_entry.get())

    def add_product(self):
        create_product(
            self.root,
            lambda: self.load_products(self.search_entry.get())
        )

    def delete_selected(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Внимание", "Выберите товар")
            return

        result = messagebox.askyesno("Подтверждение", "Удалить выбранный товар?")
        if not result:
            return

        delete_product(selected[0])
        self.load_products(self.search_entry.get())


if __name__ == "__main__":
    create_tables()
    root = tb.Window(themename="solar")
    App(root)
    root.mainloop() 
    