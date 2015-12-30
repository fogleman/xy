import math
import random

def anneal(state, max_temp, min_temp, steps):
    factor = -math.log(float(max_temp) / min_temp)
    state = state.copy()
    best_state = state.copy()
    best_energy = state.energy()
    previous_energy = best_energy
    for step in xrange(steps):
        temp = max_temp * math.exp(factor * step / steps)
        undo = state.do_move()
        energy = state.energy()
        change = energy - previous_energy
        if change > 0 and math.exp(-change / temp) < random.random():
            state.undo_move(undo)
        else:
            previous_energy = energy
            if energy < best_energy:
                # print step, temp, energy
                best_energy = energy
                best_state = state.copy()
    return best_state

def get_max_temp(state, iterations):
    state = state.copy()
    previous = state.energy()
    total = 0
    for _ in xrange(iterations):
        state.do_move()
        energy = state.energy()
        total += abs(energy - previous)
        previous = energy
    average = total / iterations
    return average * 2
