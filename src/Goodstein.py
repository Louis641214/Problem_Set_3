def to_hereditary_base(n, base):
    if n < base:
        return n
    result = []
    exp = 0
    while base ** (exp + 1) <= n:
        exp += 1
    coef = n // (base ** exp)
    rest = n % (base ** exp)
    exp_part = to_hereditary_base(exp, base)
    result.append((coef, exp_part))
    if rest > 0:
        rest_part = to_hereditary_base(rest, base)
        if isinstance(rest_part, int):
            result.append((rest_part, 0))
        else:
            result.extend(rest_part)
    return result

def replace_base(expr, old_base, new_base):
    if isinstance(expr, int):
        return expr
    replaced = []
    for coef, exp in expr:
        new_exp = replace_base(exp, old_base, new_base)
        replaced.append((coef, new_exp))
    return replaced

def evaluate(expr, base):
    if isinstance(expr, int):
        return expr
    total = 0
    for coef, exp in expr:
        total += coef * (base ** evaluate(exp, base))
    return total

def goodstein_sequence(start, base, max_steps=1000):
    sequence = [start]
    m = start
    b = base
    steps = 0
    while m != 0 and steps < max_steps:
        hereditarily = to_hereditary_base(m, b)
        replaced = replace_base(hereditarily, b, b + 1)
        m = evaluate(replaced, b + 1) - 1
        sequence.append(m)
        b += 1
        steps += 1
    return sequence