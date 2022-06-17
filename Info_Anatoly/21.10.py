def get_hiragana_string(text: string) -> str:
    
  dictionary = {'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ',
              'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご',
              'sa': 'さ', 'si': 'し', 'su': 'す', 'se': 'せ', 'so': 'そ',
              'za': 'ざ', 'zi': 'じ', 'zu': 'ず', 'ze': 'ぜ', 'zo': 'ぞ',
              'ta': 'た', 'ti': 'ち', 'tu': 'つ', 'te': 'て', 'to': 'と',
              'da': 'だ', 'di': 'ぢ', 'du': 'づ', 'de': 'で', 'do': 'ど',
              'na': 'な', 'ni': 'に', 'nu': 'ぬ', 'ne': 'ね', 'no': 'の',
              'ha': 'は', 'hi': 'ひ', 'hu': 'ふ', 'he': 'へ', 'ho': 'ほ',
              'ba': 'ば', 'bi': 'び', 'bu': 'ぶ', 'be': 'べ', 'bo': 'ぼ',
              'pa': 'ぱ', 'pi': 'ぴ', 'pu': 'ぷ', 'pe': 'ぺ', 'po': 'ぽ',
              'ma': 'ま', 'mi': 'み', 'mu': 'む', 'me': 'め', 'mo': 'も',
              'ya': 'や', 'yu': 'ゆ', 'yo': 'よ',
              'ra': 'ら', 'ri': 'り', 'ru': 'る', 're': 'れ', 'ro': 'ろ',
              'wa': 'わ', 'wi': 'ゐ', 'we': 'ゑ', 'wo': 'を',
              'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お',
              'n': 'ん'
              }


  big_ans = ''
  arg = input()
  i = 0
  new_string = arg.split(' ')
  for l in new_string:
    if ((l[0] != 'a') and (l[0] != 'i') and (l[0] != 'u') and (l[0] != 'e') and (l[0] != 'o')):
      for i in range(len(l)):
          if (i % 2 != 0):
            el1 = i - 1
            el2 = i + 1
            ans = l[el1:el2]
            big_ans += dictionary.get(ans)
      if (len(l) % 2 != 0):
        ans = l[-1]
        big_ans += dictionary.get(ans)
      big_ans += ' '


        
    else:
      ans = l[0]
      big_ans += dictionary.get(ans)
      l = l[1:]
      for i in range(len(l)):
          if (i % 2 != 0):
            el1 = i - 1
            el2 = i + 1
            ans = l[el1:el2]
            big_ans += dictionary.get(ans)
      if (len(l) % 2 != 0):
        ans = l[-1]
        big_ans += dictionary.get(ans)

          
      big_ans += ' '
  return big_ans
print(get_hiragana_string(arg))
