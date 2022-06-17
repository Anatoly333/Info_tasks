'''This module change words in given text to there synonyms, just write antonymize_text(text)'''
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator
import pymorphy2

def gramem_word(word):
    '''Putting the word in the desired form'''
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    parse = morph.parse(word)[0]
    gramem = parse.tag.grammemes
    return parse.inflect(gramem).word

def antonymize_text(text):
    '''Change text in text with antonyms'''
    translated = GoogleTranslator(source='auto', target='en').translate(text)
    translated_comma_check = ''
    translated_punctuation_check = ''
    for j in translated:
        if j == ',':
            translated_comma_check += ' '
        translated_comma_check += j
    for j in translated_comma_check:
        if j in ('.', '!', '?'):
            translated_punctuation_check += ' '
        translated_punctuation_check += j

    translated_array = translated_punctuation_check.split(' ')

    synonyms = []
    antonyms = []
    for i in range(len(translated_array)):
        for syn in wordnet.synsets(translated_array[i]):
            for j in syn.lemmas():
                synonyms.append(j.name())
                if j.antonyms():
                    antonyms.append(j.antonyms()[0].name())
                    translated_array[i] = antonyms[-1]
    translated_for_ru = ''
    flag = 0
    for i in translated_array:
        flag += 1
        if flag == 1:
            translated_for_ru = translated_for_ru + i
        else:
            if i != ',':
                translated_for_ru = translated_for_ru + ' ' + i
            else:
                translated_for_ru = translated_for_ru + i

    text = translated_for_ru
    translated = GoogleTranslator(source='auto', target='ru').translate(text)

    translated_gramem = ''
    translated_punctuation_check = ''
    for j in translated:
        if j == ',':
            translated_gramem += ' '
        translated_gramem += j
    for j in translated_gramem:
        if j in ('.', '!', '?'):
            translated_punctuation_check += ' '
        translated_punctuation_check += j

    translated_punctuation_check = translated_punctuation_check.split(' ')

    translated_gramem_ru = ''
    flag = 0
    for i in translated_punctuation_check:
        flag += 1
        if flag == 1:
            translated_gramem_ru = translated_gramem_ru + gramem_word(i).capitalize()
        else:
            if i not in (',', '!', '.', '?'):
                translated_gramem_ru = translated_gramem_ru + ' ' + gramem_word(i)
            elif i == ',':
                translated_gramem_ru = translated_gramem_ru + gramem_word(i)
            elif i in ('.', '!', '?'):
                translated_gramem_ru = translated_gramem_ru + gramem_word(i) + ' '
                flag = 0
    return translated_gramem_ru
