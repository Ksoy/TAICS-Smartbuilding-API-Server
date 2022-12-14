import random

def gen_data(shortName):
    if shortName == 'pwrDwn':
        return random.choice(('DOWN', 'UP'))
    elif shortName == 'I':
        return random.uniform(3, 5)
    elif shortName == 'V':
        return 110 + random.uniform(-2, 2)
    else:
        return random.random()
