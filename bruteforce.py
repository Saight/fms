#!/usr/bin/env python3
"""
"""
import numpy as np
import math
from readschedule import read_schedule, read_input
import time

def bruteforce(maxmachines,production_machines,pmachinesperstage,jobs,roundtime,timebetweenmachines,schedule,duration):
    best_solution = math.inf
    starttime = time.time()
    for a in range(roundtime):
        for b in range(a,roundtime):
            for c in range(b,roundtime):
                for d in range(c,roundtime):
                    for e in range(d,roundtime):
                        for f in range(e,roundtime):
                            for g in range(f,roundtime):
                                startingtime = []
                                newtime = np.zeros(roundtime)
                                newtime[0] = 1
                                startingtime.append(newtime)
                                for element in [a,b,c,d,e,f,g]:
                                    newtime = np.zeros(roundtime)
                                    newtime[element] = 1
                                    startingtime.append(newtime)
                                if read_schedule(maxmachines,production_machines,pmachinesperstage,jobs,startingtime,roundtime,timebetweenmachines,schedule,duration) < best_solution:
                                    best_solution = read_schedule(maxmachines,production_machines,pmachinesperstage,jobs,startingtime,roundtime,timebetweenmachines,schedule,duration)
                                    best_schedule = startingtime
                                if time.time()-starttime > 60:
                                    print([best_solution,best_schedule])
                                    starttime = time.time()
    return [best_solution,best_schedule]

def main():
    duration = [read_input("ptime.txt")][0]
    schedule = [read_input("pschedule.txt")][0]
    pmachinesperstage = [read_input("pmachinesperstage.txt")][0]
    print(bruteforce(8,10,pmachinesperstage,25,22,2,schedule,duration))

if __name__ == '__main__':
    main()


"""
np.set_printoptions(threshold="nan")

itertools.permutation
"""
