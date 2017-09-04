#!/usr/bin/env python3
"""
"""
from readschedule import read_schedule,read_input

def heuristic(maxvehicles,production_vehicles,pmachinesperstage,jobs,roundtime,timebetweenmachines,schedule,duration,iterations,perturbationjump):
    from readschedule import read_schedule
    import numpy as np
    from random import randint
    import math

    best_solutions = np.ones(maxvehicles)*math.inf
    best_schedule = []
    for i in range(maxvehicles):
        best_schedule.append(0)
    for vehicles in range(1,maxvehicles+1):
        """
        generating a random opening sequence

        The opening sequence is generated by taking a list of zeros the length
        of possible starting points and replacing a random one with a one for each
        of the vehicles in the given iteration. Exception: the first machine is
        set to start at 0 to increase the chance of finding a solution in which
        at least one machine starts at 0.
        """
        opening_sequence = np.zeros((vehicles, roundtime))
        opening_sequence[0,0] = 1
        for i in range(1,vehicles):
            opening_sequence[i, randint(0,roundtime-1)] = 1
        opening_solution = read_schedule(vehicles,production_vehicles,pmachinesperstage,jobs,opening_sequence,roundtime,timebetweenmachines,schedule,duration)
        best_solution = opening_solution
        best_sequence = opening_sequence
        current_solution = opening_solution
        current_sequence = opening_sequence

        for iteration in range(iterations):
            """
            perturbation

            all vehiclestartingtimes except for "0-starts" are moved to the front
            by "perturbationjump" units. If this would cause a machine to start
            earlier than "0" the machine's starting point is instead counted down
            from the back of the schedule. "0-starts" are not moved in an attempt to
            stay in optimal solution range(Cmax is regular, therefore the optimal
            solution has a vehicles start at 0)
            """
            if iteration > 0:
                opening_sequence = best_sequence
                for i in range(len(opening_sequence)):
                    if opening_sequence[i,0]!=1:
                        for j in range(perturbationjump,len(opening_sequence[0])):
                            if opening_sequence[i,j] == 1:
                                opening_sequence[i,j-perturbationjump] = 1
                                opening_sequence[i,j] = 0
                        for j in range(perturbationjump):
                            if opening_sequence[i,j] == 1:
                                opening_sequence[i,(j-perturbationjump)%roundtime] = 1
                                opening_sequence[i,j] = 0

                opening_solution = read_schedule(vehicles,production_vehicles,pmachinesperstage,jobs,opening_sequence,roundtime,timebetweenmachines,schedule,duration)
                best_solution = opening_solution
                best_sequence = opening_sequence
                current_solution = opening_solution
                current_sequence = opening_sequence
            """
            generating neighborhood solutions

            neighborhood solutions are generated by allowing every machine to
            start either one unit of time earlier or later, but only one machine
            may change at a time. This leads to 2*vehicles as the size of the
            neighborhood in each iteration
            """
            nobettersolution = 0
            while nobettersolution == 0:
                startlist=np.zeros(vehicles, dtype=int)
                for i in range(vehicles):
                    # find start of act machine i:
                    for j in range(roundtime):
                        startlist[i]+= current_sequence[i,j]*j


                for i in range(vehicles):
                    # move the 1 to the left
                    new_sequence = current_sequence.copy()
                    new_solution = 0
                    for j in range(0, roundtime):
                        if new_sequence[i,j] == 1:
                            new_sequence[i,j] = 0
                            new_sequence[i,(j-1)%roundtime] = 1
                            break
                    new_solution = read_schedule(vehicles,production_vehicles,pmachinesperstage,jobs,new_sequence,roundtime,timebetweenmachines,schedule,duration)
                    if new_solution < best_solution:
                        best_solution = new_solution
                        best_sequence = new_sequence.copy()

                for i in range(vehicles):
                    # move the 1 to the right
                    new_sequence = current_sequence.copy()
                    new_solution = 0
                    for j in range(0, roundtime):
                        if new_sequence[i,j] == 1:
                            new_sequence[i,j] = 0
                            new_sequence[i,(j+1)%roundtime] = 1
                            break
                    new_solution = read_schedule(vehicles,production_vehicles,pmachinesperstage,jobs,new_sequence,roundtime,timebetweenmachines,schedule,duration)
                    if new_solution < best_solution:
                        best_solution = new_solution
                        best_sequence = new_sequence
                """
                Accepting better solutions and breaking an iteration

                the heuristic runs until it cannot find a solution that returns
                a lower goal than the one returned in the previous iteration.
                if a better solution is found then the heuristic will generate a
                new neighborhood starting from the newly found solution
                """
                if best_solution == current_solution:
                    nobettersolution = 1
                else:
                    current_solution = best_solution
                    current_sequence = best_sequence

            if best_solution < best_solutions[vehicles-1]:
                best_solutions[vehicles-1] = best_solution
                best_schedule[vehicles-1] = best_sequence.copy()
        """
        Optimizing of returned solutions by using the regularity of the target
        function(Cmax)

        As a final step before the return of the received solutions every schedule
        is moved to make sure that the first machine does indeed start at time 0
        ([0,1,0,1] gets a strictly worse solution than [1,0,1,0], regularity
        states that the second schedule will save the unnecesserily waited unit
        of time of the first schedule, and will therefore return a better solution
        """
        if vehicles > 2:
            if best_solutions[vehicles-1] > best_solutions[vehicles-2]:
                new_sequence = np.zeros((vehicles, roundtime))
                for i in range(vehicles-1):
                    for j in range(roundtime):
                        new_sequence[i,j] = best_schedule[vehicles-2][i,j]
                new_sequence[vehicles-1, randint(0,roundtime-1)] = 1
                new_solution = read_schedule(vehicles,production_vehicles,pmachinesperstage,jobs,new_sequence,roundtime,timebetweenmachines,schedule,duration)
                print(new_solution, vehicles)
                print(new_sequence)
                if new_solution < best_solution:
                    best_solutions[vehicles-1] = new_solution
                    best_schedule[vehicles-1] = new_sequence.copy()

    return [best_solutions,best_schedule]



if __name__ == "__main__":
    #heuristic(maxvehicles,production_vehicles,pmachinesperstage,jobs,roundtime,timebetweenmachines,schedule,duration,iterations,perturbationjump)
    duration = [read_input("ptime.txt")][0]
    schedule = [read_input("pschedule.txt")][0]
    pmachinesperstage = [read_input("pmachinesperstage.txt")][0]
    printnow=heuristic(8,10,pmachinesperstage,25,22,2,schedule,duration,40,5)
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
        print("Solution with {} vehicles: {}".format(i+1,printnow[0][i]))
        print("Schedule:")
        print(schedules)
        schedules =[]
