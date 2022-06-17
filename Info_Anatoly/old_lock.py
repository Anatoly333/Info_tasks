"""Unlocking the lock, using the shortest way with dfs."""
import collections


def open_lock(target, deadends, lock_length):
    """Unlocking the lock, using the shortest way."""
    if "0000" in deadends:
        return -1

    def children(wheel):
        res = []
        for i in range(4):
            digit = str((int(wheel[i]) + 1) % 10)
            res.append(wheel[:i] + digit + wheel[i + 1:])
            digit = str((int(wheel[i]) + 10 - 1) % 10)
            res.append(wheel[:i] + digit + wheel[i + 1:])
        return res

    que = collections.deque()
    visit = set(deadends)
    que.append(["0000", 0])
    while que:
        wheel, turns = que.popleft()
        if wheel == target:
            return turns
        for child in children(wheel):
            if child not in visit:
                visit.add(child)
                que.append([child, turns + 1])


deadends = ['0001', '1000']
print(open_lock('5210', deadends, 4))
