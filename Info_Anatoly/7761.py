import random

def generate_ege_task_01():
    q = random.randint(1, 5)
    a = random.randint(10, 100)^q
    w = random.randint(1, 5)
    b = random.randint(10, 100)^w
    c = a+b-15
    d = str(bin(c))[2:]
    quantity = 0
    i = 0
    while (i <= len(d)-1):
      if (d[i] == '1'):
        quantity = quantity+1
      i = i+1
    task_text = '''Сколько единиц содержится в двоичной записи значения выражения: {} ^ {} + {} ^ {} - 15 .?

(числа справа записаны в двоичной системе счисления)'''.format(a,q,b,w)
    return d,quantity,task_text

d,quantity,task_text = generate_ege_task_01()
print(task_text)
print(d)
print(quantity)