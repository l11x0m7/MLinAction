def iterprime(limit):
    known = {2}
    yield 2
    for i in range(3, limit):
        if i <= 2:
            yield i
        for j in known:
            if i % j == 0:
                break
        else:
            known.add(i)
            yield i


for p in iterprime(1000):
    print p
