#!/usr/bin/env python3

def chance_for_roll(roll, die, exploding=True):
    '''calculate probability to obtain result roll with a single roll of a die-sided dice'''
    if roll <= 0 or not isinstance(roll, int):
        raise RuntimeError(
            f'Illegal Argument: roll needs to be a positive integer, but is {roll} of type {type(roll)}'
        )
    elif roll < die:
        return 1/die
    elif roll == die and not exploding:
        return 1/die
    elif roll > die and exploding:
        return 1/die * chance_for_roll(roll - die, die, exploding)
    else:
        return 0

def chance_in_range(lower, upper, die, exploding=True):
    '''probability to roll a result in range [lower, upper] on a Ddie'''
    chance = 0
    for i in range(lower, upper+1):
        chance += chance_for_roll(i, die, exploding)

    return chance

def chance_smaller(value, die, exploding=True):
    '''probability to roll smaller than value on a Ddie'''
    return chance_in_range(1, value-1, die, exploding)
    
def chance_equal_larger(value, die, exploding=True):
    '''probability to roll as least value on a Ddie.'''
    return 1 - chance_smaller(value, die, exploding)

if __name__ == '__main__':
    print(chance_smaller(6, 4))
    print(chance_equal_larger(6, 4))
    print(chance_for_roll(1, 6))
    print(chance_in_range(1, 4, 4, False))
    
