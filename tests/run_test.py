
def bogus(a):
    if a:
        return 1


def test_bogus():
    assert bogus(1) == 1