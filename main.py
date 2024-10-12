import sys


sys.stdin = open("input.txt", "r")
sys.stdout = open("output.txt", "w")


def in_int():  # функция для ввода целотипного числа
    return int(sys.stdin.readline())


def in_str():  # функция для ввода строки
    return sys.stdin.readline().strip()


dct = {  # определяем приоритет операций
    '>': 0,
    'v': 1,
    '&': 2,
    '_': 3
}


def my_not(x):  # функция отрицания
    if x == 1:
        return 0
    return 1


def my_implication(x, y):  # функция импликации
    if x == 0:
        return 1
    return max(0, y)


def my_or(x, y):  # функция "или"
    return max(x, y)


def my_and(x, y):  # функция "и"
    return min(x, y)


def reverse_polish_notation(f):  # обратная польская запись
    stack1 = []  # инициализируем пустой стек
    stack2 = []  # инициализируем второй пустой стек
    length = len(f)  # записываем в переменную длину строки (функцию которую ввели)
    i = 0  # счетчик для цикла
    while i < length:  # пока i меньше длины функции
        if f[i] == '_' or f[i] == '(':  # если текущий символ равен "_" или "("
            stack1.append(f[i])  # добавляем в первый стек текщий символ
        elif f[i] == ')':  # если текущий символ "("
            while stack1[-1] != '(':  # пока не встречаем из первого стека "("
                stack2.append(stack1.pop())  # добавляем во второй стек вершину первого стека
            stack1.pop()  # удаляем из вершины стека "("
        elif f[i] == 'v' or f[i] == '&' or f[i] == '>':  # если текущий символ "v" или "&" или "<"
            # пока первый стек не пустой и (элемент вершины стека в словаре и
            # приоритет вершины первого стека больше текущего операнда (f[i])
            while stack1 and (stack1[-1] in dct and dct[stack1[-1]] >= dct[f[i]]):
                stack2.append(stack1.pop())  # добавляем во второй стек вершину первого стека
            stack1.append(f[i])  # удаляем операнд из вершины первого стека
        elif f[i].isdigit():  # если текущий символ число
            stack2.append(f[i])  # добавляем число во второй стек
        i += 1  # инкрементируем счетчик (увеличиваем на 1)
    while stack1:  # пока первый стек не пуст
        stack2.append(stack1.pop())  # добавляем во второй стек вершину первого стека
    return stack2  # возврашаем второй стек


def calculate(f):  # вычисления значения функции из обратной польской записи
    stack = reverse_polish_notation(f)  # записываем обратную польскую запись в переменную
    stck = [stack[0]]  # создаем новый стек и добавим первый символ основного стека
    stack.remove(stack[0])  # удалим первый символ основного стека
    i = 0  # создаем счетчик для цикла
    while len(stack) > 0:  # пока стек не пуст
        if stack[i].isdigit():  # если stack[i] - число
            stck.append(stack[i])  # добавим в дополнительный стек это число
        elif stack[i] == '_':  # если stack[i] = "_"
            stck.append(my_not(int(stck.pop())))  # добавим в дополнительный стек результат вызова функции my_not
        elif stack[i] == '&':  # если stack[i] = "&"
            y = int(stck.pop())  # записываем вершину дополнительного стека
            x = int(stck.pop())  # записываем вершину дополнительного стека
            stck.append(my_and(x, y))  # добавим в дополнительный стек результат вызова функции my_and
        elif stack[i] == 'v':  # если stack[i] = "v"
            y = int(stck.pop())  # записываем вершину дополнительного стека
            x = int(stck.pop())  # записываем вершину дополнительного стека
            stck.append(my_or(x, y))  # добавим в дополнительный стек результат вызова функции my_or
        elif stack[i] == '>':  # если stack[i] = ">"
            y = int(stck.pop())  # записываем вершину дополнительного стека
            x = int(stck.pop())  # записываем вершину дополнительного стека
            stck.append(my_implication(x, y))  # добавим в дополнительный стек результат вызова функции my_implication
        stack.remove(stack[i])  # удалим элемент stack[i] из основного стека
    return stck[0]  # возвращаем результат вычисления


def check(f, k):  # функция перебора всех значений аргументов
    st = set()  # создаем пустое множество
    ans = []  # создаем пустой список
    for i in range(len(f)):  # перебираем по индексу все символы строки f
        if (65 <= ord(f[i]) <= 92 or 97 <= ord(f[i]) <= 122) and f[i] != 'v':  # если символ - латинская буква
            st.add(f[i])  # добавим этот символ в множество
    count = len(st)  # посчитаем кол-во переменных в функции
    st = list(st)  # преобразуем множество в список
    st.sort()  # отсортируем (лексикографически) элементы списка
    if count == 1:  # если у нас 1 переменная
        ans = [[st[0], 'f']]
        for kk in range(k):
            s = ''
            for i in range(len(f)):
                if (65 <= ord(f[i]) <= 92 or 97 <= ord(f[i]) <= 122) and f[i] != 'v':
                    s += str(kk)
                else:
                    s += f[i]

            ans.append([kk, calculate(s)])
    elif count == 2:  # если у нас 2 переменные
        ans = [[a for a in st]]
        ans[0].append('f')
        x = st[0]
        for ki in range(k):
            for kj in range(k):
                s = ''
                for i in range(len(f)):
                    if (65 <= ord(f[i]) <= 92 or 97 <= ord(f[i]) <= 122) and f[i] != 'v':
                        if f[i] == x:
                            s += str(ki)
                        else:
                            s += str(kj)
                    else:
                        s += f[i]

                ans.append([ki, kj, calculate(s)])
    elif count == 3:  # если у нас 3 переменные
        ans = [[a for a in st]]
        ans[0].append('f')
        x = st[0]
        y = st[1]
        for ki in range(k):
            for kj in range(k):
                for kk in range(k):
                    s = ''
                    for i in range(len(f)):
                        if (65 <= ord(f[i]) <= 92 or 97 <= ord(f[i]) <= 122) and f[i] != 'v':
                            if f[i] == x:
                                s += str(ki)
                            elif f[i] == y:
                                s += str(kj)
                            else:
                                s += str(kk)
                        else:
                            s += f[i]

                    ans.append([ki, kj, kk, calculate(s)])
    return ans  # возвращаем таблицу истинности функции


def analogue(arr, k):  # функция преобразовния в первой (СДНФ и СКНФ)
    # sdnf = ''
    sknf = ''  # переменная для записи СКНФ
    n = len(arr[0]) - 1
    k = 0
    for ar in arr[1:]:
        if ar[-1] == 0:
            k += 1
    for i in range(1, len(arr)):
        """
        if arr[i][-1] == 1:
            sdnf += '('
            for j in range(n):
                if arr[i][j] == 0:
                    sdnf += '_' + str(arr[0][j])
                else:
                    sdnf += str(arr[0][j])
                if j < n - 1:
                    sdnf += ' & '
            sdnf += ') v '
        """

        if arr[i][-1] == 0:  # смотрим по нулям из таблицы истинности
            sknf += '('  # добавим в строку открывающую скобку
            for j in range(n):  # перебираем все переменные функции
                if arr[i][j] == 1:  # если x == 1
                    sknf += '_' + str(arr[0][j])  # добавим в инверсном виде
                else:  # иначе
                    sknf += str(arr[0][j])  # добавим в обычном виде
                if j < n - 1:  # между переменными должна быть дизьюнкция
                    sknf += ' v '
            sknf += ')'
            if i < k:
                sknf += ' & '  # между скобками должна быть конъюнкция

    return sknf  # возвращаем СКНФ вводимой функции


def solve(s):  # функция для вызова отдельных функций
    ans = check(s, 2)
    analogue_ = analogue(ans, 2)
    return ans, analogue_


def main():  # основная функия (точка входа программы)
    f = False
    t = 1
    if f:
        t = in_int()
    for i in range(t):
        s = in_str()  # читаем вводимую функцию
        ans, analogue_ = solve(s)  # записываем результат функции solve в переменные ans и analogue_

        prev = ans[0][0]
        for row in ans:  # печатаем таблицу истинности функции
            if row[0] != prev:
                prev = row[0]
                print('-' * 3 * len(row))
            print(*row, sep=" | ")
        print('-------------------------------')
        # print("СДНФ: ", analogue_[0])
        print("СКНФ: ", analogue_)  # печатаем СКНФ


if __name__ == '__main__':
    main()
