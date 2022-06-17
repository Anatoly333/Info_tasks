def get_levenshtein_distance(first_word: str, second_word: str) -> int:
    n, m = len(first_word), len(second_word)
    if n > m:
        first_word, second_word = second_word, first_word
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if first_word[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]
first_word = input()
second_word = input()
print(distance(first_word, second_word))