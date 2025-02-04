#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib import colormaps

RESULT_CLASSES = ['Patzer', 'Fehlschlag', 'Erfolg', 'Steigerung']

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


def savage_worlds_probabilities(die, wildcard=True):
    '''return a dict with the probabilities for the individual result classes'''
    p_fumble = 1/die * (1/6 if wildcard else 1)
    p_fail = chance_smaller(4, die) * (chance_smaller(4, 6) if wildcard else 1) - p_fumble
    p_success = chance_in_range(4, 7, die)*(1 - wildcard*chance_equal_larger(8, 6)) + wildcard*chance_in_range(4, 7, 6)*chance_smaller(4, die)
    p_increment = chance_equal_larger(8, die) + wildcard*chance_equal_larger(8, 6)*chance_smaller(8, die)

    return {
        'fumble': p_fumble,
        'fail': p_fail,
        'success': p_success,
        'increment': p_increment
    }


def make_plot(dice, wildcard):
    '''
    create overlay plot of probabilities for different dice

    Creates a plot showing the different probabilities to roll a certain result class.

    dice: integer or list of integers. The number of faces on the dies.
    wildcard: bool or list of bools. Whether a wildcard die should be rolled in addition to
        the die. If this is a bool and dice is a list, the same choice is used for all dice.

    returns: the Figure and Axes objects from plt.subplots.

    '''
    fig, ax = plt.subplots()

    if type(dice) == int:
        dice = [dice]

    if type(wildcard) == bool:
        wildcard = [wildcard]*len(dice)

    for die, wc in zip(dice, wildcard):
        results = savage_worlds_probabilities(die, wc)
        nbins = len(RESULT_CLASSES)

        # repeat first and last values so that the graph extends beyond the ticks
        values = list(results.values())
        new_values = [values[0]] + values + [values[-1]]
        new_values = [100*v for v in new_values]  # percent look nicer on the plot
        label = f'W{die} (Wildcard)' if wc else f'W{die}'
        ax.step(range(nbins+2), new_values, where='mid', label=label)

    # cut the dummy values out of the plot
    ax.set_xlim(0.5, nbins+.5)
    ax.set_xticks(range(1, nbins+1), RESULT_CLASSES)
    ax.set_ylabel('Wahrscheinlichkeit [%]')
    ax.set_ylim(0, 100)
    ax.legend()

    return fig, ax


if __name__ == '__main__':

    fig, ax = make_plot([4, 6, 8, 10, 12], True)
    fig.suptitle('Ergebniswahrscheinlichkeiten bei Savage Worlds')
    fig.savefig('all_dice_wildcard.png')

    fig, ax = make_plot([4, 6, 8, 10, 12], False)
    fig.suptitle('Ergebniswahrscheinlichkeiten bei Savage Worlds')
    fig.savefig('all_dice_no_wildcard.png')

    for die in [4, 6, 8, 10, 12]:
        fig, ax = make_plot([die, die], [True, False])
        fig.suptitle('Ergebniswahrscheinlichkeiten bei Savage Worlds')
        fig.savefig(f'd{die}.png')
