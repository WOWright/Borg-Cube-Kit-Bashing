import numpy as np
import matplotlib.pyplot as plt

def quasirandom(n):
    w = len(bin(n))

    x = np.arange(n, dtype=float)
    y = np.zeros_like(x)

    for i, a in enumerate(x):
        b = bin(i)
        c = int(b[:1:-1] + (w - len(b)) * '0', 2)
        y[i] = c

    return x, y


# def l_system(N, scale, l):
#     """
#     Created on Tue Sep 26  2017
#
#     L-systems physics... done without turtle graphics
#
#         F = draw a line forward
#         + = turn right
#         - = turn left
#         [ = save position and heading (as a list)
#         ] = restore last saved poisition, pop it from list
#
#     @author: Hanchak, Mike
#     """
#     # dictionary containing the mapping rule
#     # this is a tree-like L-System (reference: The Coding Train on YouTube)
#     rule = {'F': 'F+[+F]-[-F++F-F]'}
#     # Mike's settings. Replaced with function arguments
#     # N = 7
#     # scale = 0.55
#
#     # initial condition
#     sentence = 'F'
#
#     # generate the sentence of moves
#     for i in range(N):
#         sentence = sentence.replace('F', rule['F'])
#
#     #################### pot the resulting moves as lines ####################
#     ######################### using MATPLOTLIB graphics ######################
#     #l = 1  # length of forward movement
#     ang = np.pi/4
#     # ang = 20 * np.pi / 180  # turning angle
#     pos = [(0,0)]  # initial position (list of tuples)
#     heading = [np.pi/2]    # initial heading (list of floats)
#
#     # set initial orientation and position of "pen"
#     x = 0
#     y = 0
#     th = 90 * np.pi / 180
#
#     # Now create a list of lists to save all of the x,y points for later plotting
#     points = [[] for i in range(N + 1)]
#     directions = [[] for i in range(N + 1)]
#     level = 0  # level for later coloring
#     points[level].append([x, y])
#     directions[level].append(th)
#
#     # go through the sentence one character at a time
#     for char in sentence:
#
#         if char == 'F':
#
#             x += l * np.cos(th)
#             y += l * np.sin(th)
#             points[level].append([x, y])
#             directions[level].append(th)
#
#         elif char == '+':
#
#             th -= ang
#
#         elif char == '-':
#
#             th += ang
#
#         elif char == '[':
#
#             level += 1
#             # save transformation state by append position to list
#             pos.append((x, y))
#             heading.append(th)
#
#             l = l * scale
#
#             points[level].append([np.nan, np.nan])  # break in the plotting
#             points[level].append([x, y])
#
#             directions[level].append(np.nan)
#             directions[level].append(th)
#
#         elif char == ']':
#
#             level -= 1
#
#             l = l / scale
#
#             # go to last saved position
#             # get then delete last saved position
#             x, y = pos.pop()
#             th = heading.pop()
#
#     return points, directions
