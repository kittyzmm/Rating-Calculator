import tkinter as tk
from tkinter import messagebox, scrolledtext

def parse_grades(s):
    if not s or not s.strip():
        raise ValueError("Поле ввода оценок пустое.")
    s = s.strip().replace(',', ' ').replace(';', ' ')
    grades = []
    for p in s.split():
        n = float(p)
        if n < 1 or n > 5:
            raise ValueError(f"Оценка {n} невозможна.")
        grades.append(n)
    return grades

def calculate_average(s):
    g = parse_grades(s)
    if not g:
        raise ValueError("Нет оценок для расчёта.")
    return round(sum(g) / len(g), 2), len(g)

def generate_combinations(values, count):
    if count == 0:
        return [[]]
    result = []
    for i, val in enumerate(values):
        for combo in generate_combinations(values[i:], count - 1):
            result.append([val] + combo)
    return result

def _calculate_final_avg(cs, cc, v):
    total_sum = cs + sum(v)
    total_count = cc + len(v)
    return total_sum / total_count

def predict_grades(curr, tgt, cnt):
    tgt, cnt = float(tgt), int(cnt)
    if tgt < 1 or tgt > 5:
        raise ValueError("Желаемое среднее должно быть от 1 до 5.")
    if cnt <= 0:
        raise ValueError("Количество работ должно быть положительным.")

    if curr and curr.strip():
        g = parse_grades(curr)
        cs, cc = sum(g), len(g)
        ca = cs / cc
        if ca > tgt:
            raise ValueError(f"Ваш балл ({ca:.2f}) уже выше желаемого.")
    else:
        cs, cc, ca = 0, 0, 0.0

    tc = cc + cnt
    rs = tgt * tc
    ns = rs - cs
    min_p, max_p = cnt * 3, cnt * 5

    if ns < min_p:
        raise ValueError(f"Невозможно достичь среднего {tgt}")
    if ns > max_p:
        raise ValueError(f"Невозможно достичь среднего {tgt}")

    all_combos = generate_combinations([3, 4, 5], cnt)
    variants = []

    for combo in all_combos:
        if sum(combo) >= ns:
            v = sorted(combo, reverse=True)
            if v not in variants:
                variants.append(v)
                if len(variants) >= 3:
                    break

    if not variants:
        variants.append([3] * cnt)

    def sort_key(v):
        return _calculate_final_avg(cs, cc, v)
    
    variants.sort(key=sort_key, reverse=True)

    result = []
    for i, v in enumerate(variants[:3], 1):
        fa = _calculate_final_avg(cs, cc, v)
        result.append(f"Вариант {i}: {v} — итоговый балл: {fa:.2f}.")
    return result

def add_to_history(h, r):
    h.append(r)

def get_history_display(h):

    return "\n".join(h) if h else "История пуста."

class GradeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор оценок")
        self.history = []

        tk.Label(root, text="Оценки (через пробел, запятую или точку с запятой):").grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_grades = tk.Entry(root, width=50)
        self.entry_grades.grid(row=0, column=1, padx=5, pady=5)

        self.btn_calculate = tk.Button(root, text="Рассчитать среднее", command=self.calculate_average)
        self.btn_calculate.grid(row=1, column=0, columnspan=2, pady=5)

        self.label_result = tk.Label(root, text="", fg="blue")
        self.label_result.grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(root, text="Желаемый средний балл").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_target = tk.Entry(root, width=10)
        self.entry_target.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(root, text="Количество будущих работ:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_count = tk.Entry(root, width=10)
        self.entry_count.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.btn_predict = tk.Button(root, text="Предсказать необходимые оценки", command=self.predict_grades)
        self.btn_predict.grid(row=5, column=0, columnspan=2, pady=5)

        self.label_prediction = tk.Label(root, text="", fg="green")
        self.label_prediction.grid(row=6, column=0, columnspan=2, pady=5)

        tk.Label(root, text="История:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.text_history = scrolledtext.ScrolledText(root, height=10, width=60)
        self.text_history.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        self.update_history()

    def calculate_average(self):
        try:
            input_str = self.entry_grades.get()
            avg, count = calculate_average(input_str)
            result_text = f"Среднее: {avg} (по {count} оценкам)"
            self.label_result.config(text=result_text, fg="blue")

            record = f"Расчёт среднего: {input_str} → {avg}"
            add_to_history(self.history, record)
            self.update_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            self.label_result.config(text="", fg="blue")

    def predict_grades(self):
        try:
            current_input = self.entry_grades.get()
            target_str = self.entry_target.get()
            count_str = self.entry_count.get()

            if not target_str or not count_str:
                raise ValueError("Заполните поля 'Желаемый средний балл' и 'Количество будущих работ'.")

            avg_needed = predict_grades(current_input, target_str, count_str)
            result_text = "\n".join(avg_needed)
            self.label_prediction.config(text=result_text, fg="green")

            record = f"Необходимо {result_text}"
            add_to_history(self.history, record)
            self.update_history()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            self.label_prediction.config(text="", fg="green")

    def update_history(self):
        display = get_history_display(self.history)
        self.text_history.delete(1.0, tk.END)
        self.text_history.insert(tk.END, display)

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculatorApp(root)
    root.mainloop()
