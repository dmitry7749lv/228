import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from products import add_product


class ProductForm(tb.Toplevel):

    def __init__(self, parent, callback):
        super().__init__(parent)

        self.callback = callback

        self.title("Добавление товара")
        self.geometry("500x450")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.place_window_center()

        container = tb.Frame(self, padding=25)
        container.pack(fill=BOTH, expand=True)

        tb.Label(
            container,
            text="Новый товар",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(0, 25))

        tb.Label(container, text="Артикул").pack(anchor=W)
        self.article_entry = tb.Entry(container)
        self.article_entry.pack(fill=X, pady=(0, 15), ipady=5)

        tb.Label(container, text="Название").pack(anchor=W)
        self.name_entry = tb.Entry(container)
        self.name_entry.pack(fill=X, pady=(0, 15), ipady=5)

        tb.Label(container, text="Цена").pack(anchor=W)
        self.price_entry = tb.Entry(container)
        self.price_entry.pack(fill=X, pady=(0, 15), ipady=5)

        tb.Label(container, text="Количество").pack(anchor=W)
        self.quantity_entry = tb.Entry(container)
        self.quantity_entry.pack(fill=X, pady=(0, 25), ipady=5)

        tb.Button(
            container,
            text="Сохранить",
            bootstyle=SUCCESS,
            command=self.save
        ).pack(fill=X, ipady=8)

    def place_window_center(self):
        self.update_idletasks()

        width = 600
        height = 750

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

    def save(self):
        article = self.article_entry.get().strip()
        name = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()

        if not article or not name or not price or not quantity:
            messagebox.showwarning(
                "Ошибка",
                "Заполните все поля"
            )
            return

        if len(article) < 3:
            messagebox.showwarning(
                "Ошибка",
                "Артикул должен содержать минимум 3 символа"
            )
            return

        if len(name) < 2:
            messagebox.showwarning(
                "Ошибка",
                "Название товара слишком короткое"
            )
            return

        try:
            price = float(price)

            if price <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Ошибка",
                "Цена должна быть положительным числом"
            )
            return

        try:
            quantity = int(quantity)

            if quantity < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Ошибка",
                "Количество должно быть целым числом"
            )
            return

        add_product(
            article,
            name,
            price,
            quantity
        )

        self.callback()
        self.destroy()