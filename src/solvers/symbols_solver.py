import features.symbols as symbols_features

COLUMNS = [
    [0, 1, 2, 3, 4, 5, 6],
    [7, 0, 6, 8, 9, 5, 10],
    [11, 12, 8, 13, 14, 2, 9],
    [15, 16, 17, 4, 13, 10, 18],
    [19, 18, 17, 20, 16, 21, 22],
    [15, 7, 23, 24, 19, 25, 26]
]

def solve(image, model):
    symbols, coords = symbols_features.get_symbols(image, model)
    column = 0
    for i in range(6):
        if set(symbols).issubset(COLUMNS[i]):
            column = i
            break
    try:
        zipped = sorted(zip(symbols, coords), key=lambda a: COLUMNS[column].index(a[0]))
        return [c for (s, c) in zipped]
    except ValueError:
        return None
