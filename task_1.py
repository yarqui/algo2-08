import random
import time
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: tuple) -> int:
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: tuple, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right, cache):
    key = (left, right)
    cached_sum = cache.get(key)
    if cached_sum != -1:
        return cached_sum
    else:
        actual_sum = sum(array[left : right + 1])
        cache.put(key, actual_sum)
        return actual_sum


def update_with_cache(array, index, value, cache):
    array[index] = value
    keys_to_delete = []
    for key in cache.cache:
        if key[0] <= index <= key[1]:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del cache.cache[key]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


if __name__ == "__main__":
    N = 100000
    Q = 50000
    K = 1000

    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    # --- Test without cache ---
    array_no_cache = list(array)
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array_no_cache, query[1], query[2])
        elif query[0] == "Update":
            update_no_cache(array_no_cache, query[1], query[2])
    end_time = time.time()
    time_no_cache = end_time - start_time

    # --- Test with LRU cache ---
    array_with_cache = list(array)
    lru_cache = LRUCache(K)
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array_with_cache, query[1], query[2], lru_cache)
        elif query[0] == "Update":
            update_with_cache(array_with_cache, query[1], query[2], lru_cache)
    end_time = time.time()
    time_with_cache = end_time - start_time

    print(f"Without cache: {time_no_cache:.2f} s")
    if time_with_cache > 0:
        print(
            f"LRU cache    : {time_with_cache:.2f} s (speedup ×{time_no_cache/time_with_cache:.1f})"
        )
    else:
        print(f"LRU cache    : {time_with_cache:.2f} s")
