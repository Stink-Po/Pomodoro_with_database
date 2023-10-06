a = range(100)


def start():
    s = []
    for i in range(100):
        yield i
        if i % 2 == 0:
            s.append(i)

    return s


b = start()
print(b)
