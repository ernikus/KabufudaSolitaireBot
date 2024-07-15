#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyautogui as guilib
import numpy as np
import mss, os, time
import cv2 as cv
from matplotlib import pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import read, solve

MONITOR = 0

sct = mss.mss()

def get_screenshot(region=None):
    arr = np.array(sct.grab(sct.monitors[MONITOR]))[:,:,:3]
    if region:
        return arr[region[1]:region[3], region[0]:region[2]]
    return arr

def click(x, y):
    m = sct.monitors[MONITOR]
    guilib.mouseDown(m['left'] + x, m['top'] + y)
    guilib.mouseUp()

def inputSln(sln, topleft):
    if sln.fromAction is None:
        return

    inputSln(sln.parent, topleft)
    for loc in (sln.fromAction, sln.toAction):
        if loc[0] == 'stack':
            click(topleft[0] + read.cardloffset * loc[1] + read.cardroffset//2,
                topleft[1] + read.cardboffset * loc[2] + read.cardboffset//2)
        
        else:
            click(topleft[0] + read.spotroffset * loc[1] + read.spotloffset, topleft[1] + read.spotyoffset)

def export_solution_to_txt(sln, filename='solution.txt'):
    steps = []
    def collect_steps(solution):
        if solution.parent:
            collect_steps(solution.parent)
        steps.append(f"Move from {solution.fromAction} to {solution.toAction}")

    collect_steps(sln)

    with open(filename, 'w') as f:
        for step in steps:
            f.write(step + '\n')

def main():
    guilib.PAUSE = 0.015
    time.sleep(5)
    while True:
        guilib.keyDown('ctrl')
        guilib.keyDown('n')
        guilib.keyUp('n')
        guilib.keyUp('ctrl')
        coords = read.findimage(read.cv.imread('images/expert.png'))
        click(coords[0]+75, coords[1]+75)
        time.sleep(6)

        board, topleft = read.getBoard()
        print(f"Read board: {board}")
        sln = solve.solveGame(board)
        if sln is not None:
            export_solution_to_txt(sln)

if __name__ == '__main__':
    main()
