'''
This module contains Cesar cipher
'''
with open('King.txt', encoding='utf8') as f:
    TEXTF = str(f.readlines())
RUSSIAN_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def get_shifted_letter(letter: str, shift: int, alphabet: str) -> str:
    '''
    Working with a shift
    '''
    index = alphabet.find(letter.lower())
    if index == -1:
        return letter
    new_index = (index + shift) % len(alphabet)
    if letter.islower():
        return alphabet[new_index]
    return alphabet[new_index].upper()


def find_bigrams(text):
    '''
    bigrams cipher
    '''
    list_bigrams = []
    bigram = ""
    for i in text:
        if i.lower() not in RUSSIAN_ALPHABET:
            bigram = ''
            continue
        if len(bigram) < 3:
            bigram += i.lower()
        else:
            list_bigrams.append(bigram)
            bigram = bigram[1::] + i.lower()
    dict_bigrams = {}
    for j in list_bigrams:
        if j not in dict_bigrams.keys():
            dict_bigrams[j] = list_bigrams.count(j)
    return sorted(dict_bigrams.items(), key=lambda item: item[1])


def encr(text, alphabet, shift):
    '''
    encr function
    '''
    ans = ''
    for j in text:
        ans += get_shifted_letter(j, shift, alphabet)
    return ans


def decode(text):
    '''
    Decoding function
    '''
    if len(text) < 5:
        return text
    ans = ''
    shifts = {}
    all_bigrams = find_bigrams(TEXTF)
    encoded_bigrams = find_bigrams(text)
    for encoded_bigram in encoded_bigrams:
        for norm_bigram in all_bigrams:
            first_different = ord(encoded_bigram[0][0]) - ord(norm_bigram[0][0])
            second_different = ord(encoded_bigram[0][1]) - ord(norm_bigram[0][1])
            third_different = ord(encoded_bigram[0][2]) - ord(norm_bigram[0][2])
            if first_different == second_different == third_different:
                if first_different in shifts.keys():
                    shifts[first_different] += 1
                else:
                    shifts[first_different] = 1
    sorted_shifts = sorted(shifts.items(), key=lambda item: item[1])
    if len(sorted_shifts) == 0:
        return text
    shift = list(sorted_shifts[-1])[0]
    for letter in text:
        if letter.lower() not in RUSSIAN_ALPHABET:
            ans += letter
            continue
        ind = RUSSIAN_ALPHABET.find(letter.lower())
        new_index = (ind - shift) % len(RUSSIAN_ALPHABET)
        if letter.islower():
            ans += RUSSIAN_ALPHABET[new_index]
        else:
            ans += RUSSIAN_ALPHABET[new_index].upper()
    return ans
print(decode('Лбмэлфмаупс щйхсфёу гцпеопк уёлту об сфттлпн аиьлё гтёнй гпинпзоьнй лпнвйобчйанй щйхсб'))
