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