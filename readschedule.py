#!/usr/bin/env python3

def read_input(inputfile):
    import ast
    schedule = []
    with open(inputfile) as data:
        schedule = ast.literal_eval(data.read())
    return schedule

def read_schedule(machines,production_machines,pmachinesperstage,jobs,startingtime,roundtime,timebetweenmachines,schedule,duration):
    #               int            int              array         int    matrix       int          int            matrix   matrix
    """
    imports
    """
    import numpy as np
    import time
    """
    Definitions of opening variables
    """
    stopwatch = -1
    started_schedule = np.zeros(production_machines)
    inqueue = [[] for i in range(0,production_machines)]
    outqueue = [[] for i in range(0,production_machines)]
    machine_load = np.zeros(machines)
    production_finish = [np.zeros(pmachinesperstage[i]) for i in range(production_machines)]
    production_load = [np.zeros(pmachinesperstage[i]) for i in range(production_machines)]
    depot_out = jobs
    depot_in = 0
    depot_outqueue = []
    startmachine = np.zeros(machines)
    list_of_jobs = []

    for i in range(0,jobs):
        depot_outqueue.append(i+1)

    for m in range(0,machines):
        for l in range(0,roundtime):
            startmachine[m] += startingtime[m][l]*l

    for i in range(0,jobs):
        list_of_jobs.append(i+1)
    schedule.append(list_of_jobs)

    while depot_in < jobs:
        stopwatch+=1
        for m in range(0,machines):
            position = ((stopwatch-startmachine[m])%roundtime)/timebetweenmachines
            if position == 0:
                if machine_load[m] > 0:
                    depot_in += 1
                    machine_load[m] = 0
                if machine_load[m] == 0:
                    if depot_out > 0:
                        take_job = 0
                        tries = 0
                        while take_job == 0 and tries < jobs:
                            if schedule[0][tries] in depot_outqueue:
                                take_job = schedule[0][tries]
                                machine_load[m]=take_job
                                depot_outqueue.remove(take_job)
                                depot_out-=1
                                break
                            else:
                                tries += 1
            elif position%1 == 0:
                position = int(position)
                if machine_load[m] > 0:
                    inqueue[position-1].append(machine_load[m])
                    machine_load[m] = 0
                if machine_load[m] == 0:
                    if len(outqueue[position-1]) > 0:
                        take_job = 0
                        tries = 0
                        while take_job == 0 and tries < jobs:
                            if schedule[position][tries] in outqueue[position-1]:
                                take_job = schedule[position][tries]
                                machine_load[m]=take_job
                                outqueue[position-1].remove(take_job)
                                break
                            else:
                                tries += 1
        for p in range(0,production_machines):
            for s in range(0,pmachinesperstage[p]):
                if production_load[p][s] > 0:
                    if production_finish[p][s] <= stopwatch:
                        outqueue[p].append(production_load[p][s])
                        production_load[p][s] = 0
                if production_load[p][s] == 0:
                    if len(inqueue[p]) > 0:
                        next_job = (schedule[p][int(started_schedule[p])])
                        if next_job in inqueue[p]:
                            production_load[p][s] = next_job
                            production_finish[p][s] = stopwatch+duration[p][next_job-1]
                            inqueue[p].remove(next_job)
                            started_schedule[p] += 1
    """
    Final display and return
    """
    schedule.pop(production_machines)
    return stopwatch

def main():
    #heuristic(maxmachines,production_machines,pmachinesperstage,jobs,roundtime,timebetweenmachines,schedule,duration,iterations)
    read_schedule(2,3,[4,2,1],3,[[1,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])
    read_schedule(2,3,[4,2,1],3,[[0,0,1,0,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])
    read_schedule(2,3,[4,2,1],3,[[0,1,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])
    read_schedule(2,3,[4,2,1],3,[[1,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])
    read_schedule(2,3,[4,2,1],3,[[0,0,0,1,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])


if __name__ == '__main__':
    main()
