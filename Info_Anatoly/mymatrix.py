import copy


class MyMatrix:
    def __init__(self, data: list):
        self.__data = copy.deepcopy(data)

    def get_data(self):
        return copy.deepcopy(self.__data)

    def __repr__(self):
        m_n = len(str(max(list(filter((lambda x: max(x)), [x for x in self.__data]))))) + 1
        for i in range(len(self.__data)):
            copy_of_data = copy.deepcopy(self.__data[i])
            str_data = [str(x) for x in copy_of_data]
            for j in range(len(str_data)):
                # if j != 0:
                if len(str_data[j]) != m_n:
                    str_data[j] = ' ' * (m_n - len(str_data[j])) + str_data[j]
                another_list = ' '.join(str_data)
            m = '\n'.join(another_list)
        return m

    def size(self):
        if len(self.__data) == 0:
            return (0, 0)
        return (len(self.__data), len(self.__data[0]))

    def flip_up_down(self):
        self.__data.reverse()
        return self

    def flip_left_right(self):
        [x.reverse() for x in self.__data]
        return self

    def flipped_up_down(self):
        return MyMatrix(copy.deepcopy(self.__data)).flip_up_down()

    def flipped_left_right(self):
        return MyMatrix(copy.deepcopy(self.__data)).flip_left_right()

    def transpose(self):
        self.__data = list(zip(*self.__data))
        self.__data = [list(x) for x in self.__data]
        return self

    def transposed(self):
        return MyMatrix(copy.deepcopy(self.__data)).transpose()

    def __add__(self, other):
        if self.size() != other.size():
            raise ValueError('Different size')
        else:
            m = copy.deepcopy(self.__data)
            for i in range(len(self.__data)):
                for j in range(len(self.__data[i])):
                    m[i][j] += other.__data[i][j]
            return MyMatrix(m)

    def __sub__(self, other):
        if self.size() != other.size():
            raise ValueError('Different size')
        else:
            m = copy.deepcopy(self.__data)
            for i in range(len(self.__data)):
                for j in range(len(self.__data[i])):
                    m[i][j] -= other.__data[i][j]
            return MyMatrix(m)

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __getitem__(self, item):
        if type(item) == tuple:
            print("getitem tuple")
            return self.__data[item[0]][item[1]]
        else:
            print("getitem int")
            print(item)
            return self.__data[item]

    def __setitem__(self, item, value):
        if type(item) == tuple:
            print("setitem tuple")
            self.__data[item[0]][item[1]] = value
        else:
            print("setitem int")
            print(item)
            self.__data[item] = value
