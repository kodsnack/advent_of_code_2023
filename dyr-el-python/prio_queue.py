import heapq

class PrioQueue:

    def __init__(self, initial_contents=None, comparison_key=None):
        self._data = list(initial_contents) if initial_contents is not None else []
        self._key = comparison_key
        if self._key is not None:
            self._data = [(self._key(item), item) for item in self._data]
        else:
            self._data = [(item, item) for item in self._data]
        heapq.heapify(self._data)

    def push(self, item):
        key = item if self._key is None else self._key(item)
        heapq.heappush(self._data, (key, item))

    def pop(self):
        _, item = heapq.heappop(self._data)
        return item
    
    def pushpop(self, item):
        key = item if self._key is None else self._key(item)
        _, item = heapq.heappushpop(self._data, (key, item))
        return item
    
    def replace(self, item):
        key = item if self._key is None else self._key(item)
        _, item = heapq.heapreplace(self._data, (key, item))
        return item