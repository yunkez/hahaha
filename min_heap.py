class MinHeap:
    def __init__(self, arr=[]):
        self.arr = arr
        self.keys = {}
        n = len(self.arr)

        if not n == 0:
            for i in range(n):
                self.keys[self.arr[i]] = i
            for i in range(n // 2, -1, -1):
                self.min_heapify(i)

    def insert(self, x):
        # where x will go
        i = len(self.arr)
        # actual insert
        self.arr.append(x)
        self.keys[x] = i
        # keep invariant
        self.swim(i)

    def min_heapify(self, parent):
        # if no left child return
        if not 2 * parent + 1 < len(self.arr):
            return

        # if no right child
        if not 2 * parent + 2 < len(self.arr):
            x = 2 * parent + 1

        # get index of x child
        elif self.arr[2 * parent + 1] < self.arr[2 * parent + 2]:
            x = 2 * parent + 1
        else:
            x = 2 * parent + 2

        # if x than parent, swap
        if self.arr[x] < self.arr[parent]:
            self.arr[parent], self.arr[x] = self.arr[x], self.arr[parent]
            self.keys[self.arr[parent]], self.keys[self.arr[x]] = self.keys[self.arr[x]], self.keys[self.arr[parent]]

            self.min_heapify(x)

    def min(self):
        return self.arr[0]

    def delete_min(self):
        # swap min with last element
        min = self.arr[0]
        i = len(self.arr) - 1
        self.arr[0], self.arr[i] = self.arr[i], self.arr[0]
        self.keys[self.arr[0]], self.keys[self.arr[i]] = self.keys[self.arr[i]], self.keys[self.arr[0]]

        self.keys.pop(self.arr[i])
        # remove min from array
        self.arr.pop()

        # fix invariant
        self.min_heapify(0)
        return min

    def swim(self, x):
        # go up while invariant is violated
        while x > 0:
            if not self.arr[x] < self.arr[(x - 1) // 2]:
                break
            self.arr[(x - 1) // 2], self.arr[x] = self.arr[x], self.arr[(x - 1) // 2]
            self.keys[self.arr[(x-1) // 2]], self.keys[self.arr[x]] = self.keys[self.arr[x]], self.keys[self.arr[(x-1) // 2]]
            x = (x - 1) // 2

    def decrease_key(self, x, smaller_x):
        i = self.keys[x]
        self.keys.pop(self.arr[i])
        self.arr[i] = smaller_x
        self.keys[smaller_x] = i
        self.swim(i)

#
h = MinHeap([532, 234, 324, 23, 0, 3, 6, 23, 4, 6, 89, 20])

print(h.min())
print(h.arr)
print(h.keys)
# assert True, is_min_heap(h.arr)
#
# h.decrease_key(532, 1)
# print(h.arr)
# print(h.keys)
#
# assert True, is_min_heap(h.arr)