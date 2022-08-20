import ctypes

class Array:
    def __init__(self, size):
        assert size > 0, "Size must be greater than 0"

        myArray = ctypes.py_object * size
        self.size = size
        self._items = myArray()
        self._lastIdx = 0
        self.Clear(None)

    def __len__(self):
        return self.size

    def __setitem__(self, key, value):
        self._items[key] = value

    def __getitem__(self, index):
        return self._items[index]

    def Clear(self, value):
        for i in range(self.size):
            self._items[i] = value

    def __str__(self):
        m_string = "["
        for i in range(len(self._items)):
            m_string += str(self._items[i])
            m_string += ", " if i != len(self._items) - 1 else ""
        m_string += "]"
        return m_string

    def __iter__(self):
        return self._ArrayIterator(self._items)

    class _ArrayIterator:
        def __init__(self, arr):
            self._m_array = arr
            self._currIndex = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self._currIndex < len(self._m_array):
                item = self._m_array[self._currIndex]
                self._currIndex += 1
                return item
            else:
                raise StopIteration
