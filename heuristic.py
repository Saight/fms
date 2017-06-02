#!/usr/bin/env python3
"""
"""
from readschedule import read_schedule,read_input

def heuristic(maxmachines,production_machines,pmachinesperstage,jobs,roundtime,timebetweenmachines,schedule,duration,iterations):
    from readschedule import read_schedule
    import numpy as np
    from random import randint
    import math

    best_solutions = np.ones(maxmachines)*math.inf
    best_schedule = []
    for i in range(maxmachines):
        best_schedule.append(0)
    for machines in range(1,maxmachines+1):
        for iteration in range(iterations):
            """
            generating a random opening sequence
            """
            opening_sequence = np.zeros((machines, roundtime))
            opening_sequence[0,0] = 1
            for i in range(1,machines):
                opening_sequence[i, randint(0,roundtime-1)] = 1
            opening_solution = read_schedule(machines,production_machines,pmachinesperstage,jobs,opening_sequence,roundtime,timebetweenmachines,schedule,duration)
            best_solution = opening_solution
            best_sequence = opening_sequence
            current_solution = opening_solution
            current_sequence = opening_sequence
            """
            generating neighborhood solutions
            """
            nobettersolution = 0
            while nobettersolution == 0:
                startlist=np.zeros(machines, dtype=int)
                for i in range(machines):
                    # find start of act machine i:
                    for j in range(roundtime):
                        startlist[i]+= current_sequence[i,j]*j


                for i in range(machines):
                    # move the 1 to the left
                    new_sequence = current_sequence.copy()
                    new_solution = 0
                    for j in range(0, roundtime):
                        if new_sequence[i,j] == 1:
                            new_sequence[i,j] = 0
                            new_sequence[i,(j-1)%roundtime] = 1
                            break
                    new_solution = read_schedule(machines,production_machines,pmachinesperstage,jobs,new_sequence,roundtime,timebetweenmachines,schedule,duration)
                    if new_solution < best_solution:
                        best_solution = new_solution
                        best_sequence = new_sequence.copy()

                for i in range(machines):
                    new_sequence = current_sequence.copy()
                    new_solution = 0
                    for j in range(0, roundtime):
                        if new_sequence[i,j] == 1:
                            new_sequence[i,j] = 0
                            new_sequence[i,(j+1)%roundtime] = 1
                            break
                    new_solution = read_schedule(machines,production_machines,pmachinesperstage,jobs,new_sequence,roundtime,timebetweenmachines,schedule,duration)
                    if new_solution < best_solution:
                        best_solution = new_solution
                        best_sequence = new_sequence

                if best_solution == current_solution:
                    nobettersolution = 1
                else:
                    current_solution = best_solution
                    current_sequence = best_sequence

            if best_solution < best_solutions[machines-1]:
                best_solutions[machines-1] = best_solution
                best_schedule[machines-1] = best_sequence.copy()

        if machines > 2:
            if best_solutions[machines-1] > best_solutions[machines-2]:
                new_sequence = np.zeros((machines, roundtime))
                for i in range(machines-1):
                    for j in range(roundtime):
                        new_sequence[i,j] = best_schedule[machines-2][i,j]
                new_sequence[machines-1, randint(0,roundtime-1)] = 1
                new_solution = read_schedule(machines,production_machines,pmachinesperstage,jobs,new_sequence,roundtime,timebetweenmachines,schedule,duration)
                print(new_solution, machines)
                print(new_sequence)
                if new_solution < best_solution:
                    best_solutions[machines-1] = new_solution
                    best_schedule[machines-1] = new_sequence.copy()

    return [best_solutions,best_schedule]



if __name__ == "__main__":
    #heuristic(maxmachines,production_machines,pmachinesperstage,jobs,roundtime,timebetweenmachines,schedule,duration,iterations)
    duration = [read_input("ptime.txt")][0]
    schedule = [read_input("pschedule.txt")][0]
    pmachinesperstage = [read_input("pmachinesperstage.txt")][0]
    printnow=heuristic(8,10,pmachinesperstage,25,22,2,schedule,duration,40)
    schedules = []
    startsum = 0
    for i in range(len(printnow[1])):
        for k in range(len(printnow[1][0][0])):
            for j in range(len(printnow[1][i])):
                startsum += printnow[1][i][j][k]
            schedules.append(int(startsum))
            startsum = 0
        while schedules[0] < 1:
            for j in range(len(schedules)):
                if schedules[j] >= 1:
                    schedules[j-1] = schedules[j]
                    schedules[j] = 0
            printnow[0][i] -= 1
        print("Lösung mit {} Maschinen: {}".format(i+1,printnow[0][i]))
        print("Schedule:")
        print(schedules)
        schedules =[]
