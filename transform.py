def transform_led(ind):
    x = ind / 10
    #y = ind % 10

    if x % 2 == 0:
        y = 9 - (ind % 10)
    else:
        y = ind % 10

    return (x, y)

def reverse_led((x, y)):
    if x % 2 == 0:
        ind = y + x*10
    else:
        ind = (9 - y) + x*10
    return ind

