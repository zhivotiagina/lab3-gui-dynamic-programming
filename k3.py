import tkinter as tk
from tkinter import messagebox, ttk

class InvestmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №3")
        self.root.geometry("1000x700")

        self.n = 0
        self.b = 0
        self.entries = []

        self.create_top_frame()

    def create_top_frame(self):
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="Количество предприятий (n):").grid(row=0, column=0, sticky="w")
        self.n_entry = tk.Entry(top_frame, width=10)
        self.n_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Количество распределяемых средств (b):").grid(row=0, column=2, sticky="w")
        self.b_entry = tk.Entry(top_frame, width=10)
        self.b_entry.grid(row=0, column=3, padx=5)

        tk.Button(top_frame, text="Создать таблицу", command=self.create_table).grid(row=0, column=4, padx=10)
        tk.Button(top_frame, text="Решить задачу", command=self.solve).grid(row=0, column=5, padx=10)

        info_text = (
            "Введите n — число предприятий, b — общий объём средств.\n"
            "Далее заполните таблицу: для каждого предприятия укажите прирост прибыли\n"
            "при вложении 0, 1, 2, ..., b денежных единиц."
        )
        tk.Label(top_frame, text=info_text, fg="blue", justify="left").grid(
            row=1, column=0, columnspan=6, sticky="w", pady=10
        )

        self.table_frame = tk.Frame(self.root, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(self.root, height=15, wrap="word")
        self.result_text.pack(fill="both", padx=10, pady=10, expand=False)

    def create_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.entries = []

        try:
            self.n = int(self.n_entry.get())
            self.b = int(self.b_entry.get())

            if self.n <= 0 or self.b < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные целые значения n и b.")
            return

        tk.Label(self.table_frame, text="Предприятие / Вложение", borderwidth=1, relief="solid", width=20).grid(row=0, column=0)

        for j in range(self.b + 1):
            tk.Label(self.table_frame, text=str(j), borderwidth=1, relief="solid", width=10).grid(row=0, column=j + 1)

        for i in range(self.n):
            tk.Label(
                self.table_frame,
                text=f"Предприятие {i + 1}",
                borderwidth=1,
                relief="solid",
                width=20
            ).grid(row=i + 1, column=0)

            row_entries = []
            for j in range(self.b + 1):
                entry = tk.Entry(self.table_frame, width=10, justify="center")
                entry.grid(row=i + 1, column=j + 1)
                entry.insert(0, "0")
                row_entries.append(entry)
            self.entries.append(row_entries)

    def solve(self):
        if not self.entries:
            messagebox.showerror("Ошибка", "Сначала создайте таблицу.")
            return

        try:
            profits = []
            for i in range(self.n):
                row = []
                for j in range(self.b + 1):
                    value = int(self.entries[i][j].get())
                    if value < 0:
                        raise ValueError
                    row.append(value)
                profits.append(row)
        except ValueError:
            messagebox.showerror("Ошибка", "Все значения таблицы должны быть целыми неотрицательными числами.")
            return


        dp = [[0] * (self.b + 1) for _ in range(self.n)]
        choice = [[0] * (self.b + 1) for _ in range(self.n)]


        for budget in range(self.b + 1):
            dp[0][budget] = profits[0][budget]
            choice[0][budget] = budget

            for i in range(1, self.n):
                for budget in range(self.b + 1):
                    max_profit = -1
                    best_x = 0
                    for x in range(budget + 1):
                        current = profits[i][x] + dp[i - 1][budget - x]
                        if current > max_profit:
                            max_profit = current
                            best_x = x
                    dp[i][budget] = max_profit
                    choice[i][budget] = best_x


        distribution = [0] * self.n
        remaining_budget = self.b

        for i in range(self.n - 1, -1, -1):
            distribution[i] = choice[i][remaining_budget]
            remaining_budget -= distribution[i]


        self.result_text.delete(1.0, tk.END)

        self.result_text.insert(tk.END, "РЕЗУЛЬТАТ РЕШЕНИЯ\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")

        self.result_text.insert(
            tk.END,
            f"Максимальный суммарный прирост прибыли: {dp[self.n - 1][self.b]}\n\n"
        )

        self.result_text.insert(tk.END, "Оптимальное распределение средств:\n")
        for i in range(self.n):
            self.result_text.insert(
                tk.END,
                f"  Предприятие {i + 1}: {distribution[i]} ед.\n"
            )

        self.result_text.insert(tk.END, "\nТаблица динамического программирования:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")

        for i in range(self.n):
            self.result_text.insert(tk.END, f"F({i + 1}, ξ): {dp[i]}\n")

        self.result_text.insert(tk.END, "\nПояснение:\n")
        self.result_text.insert(
            tk.END,
            "Программа перебирает все возможные варианты распределения бюджета\n"
            "между предприятиями и с помощью динамического программирования\n"
            "находит такой вариант, при котором суммарный прирост прибыли максимален.\n"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()