#!/usr/bin/env python3

def read_input(inputfile):
    import ast
    schedule = []
    with open(inputfile) as data:
        schedule = ast.literal_eval(data.read())
    return schedule

def fcfs(vehicles,production_machines,pmachinesperstage,jobs,startingtime,roundtime,timebetweenmachines,schedule,duration):
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
    inqueue = [[] for i in range(0,production_machines)]
    outqueue = [[] for i in range(0,production_machines)]
    machine_load = np.zeros(vehicles)
    production_finish = [np.zeros(pmachinesperstage[i], dtype=np.int) for i in range(production_machines)]
    production_load = [np.zeros(pmachinesperstage[i], dtype=np.int) for i in range(production_machines)]
    depot_out = jobs
    depot_in = 0
    depot_outqueue = []
    startmachine = np.zeros(vehicles, dtype=np.int)
    list_of_jobs = []
    new_schedule = []
    new_schedule_counter = np.zeros(production_machines, dtype=np.int)
    position = np.zeros(vehicles, dtype=np.int)

    for i in range(0,production_machines):
        new_schedule.append(np.zeros(jobs))

    for i in range(0,jobs):
        depot_outqueue.append(i+1)

    for m in range(0,vehicles):
        for l in range(-1,roundtime):
            startmachine[m] += int(startingtime[m][l]*l)

    for m in range(vehicles):
        position[m] = (-1-startmachine[m])%roundtime

#    for i in range(0,jobs):
#        list_of_jobs.append(i+1)
#    schedule.append(list_of_jobs)
    """
    Iterative check of workload of vehicles and production machines per unit of
    time

    At each time unit the position and load of each vehicle is checked and jobs
    are unloaded/picked up at the production machines. The calculation runs until
    all the jobs have been processed at all production machines and have been
    returned to the depot.
    """
    while depot_in < jobs:
        stopwatch+=1
        for p in range(0,production_machines):
            for s in range(0,pmachinesperstage[p]):
                if production_load[p][s] > 0:
                    if production_finish[p][s] <= stopwatch:
                        outqueue[p].append(production_load[p][s])
                        production_load[p][s] = 0
        for m in range(0,vehicles):
            position[m] = (position[m]+1)%roundtime
            if position[m] == 0:
                if machine_load[m] > 0:
                    depot_in += 1
                    machine_load[m] = 0
                if machine_load[m] == 0:
                    if depot_out > 0:
                        take_job = depot_outqueue[0]
                        machine_load[m] = int(take_job)
                        depot_outqueue.remove(take_job)
                        depot_out-=1
            elif position[m]%timebetweenmachines == 0:
                if machine_load[m] > 0:
                    inqueue[position[m]//timebetweenmachines-1].append(int(machine_load[m]))
                    machine_load[m] = 0
                if machine_load[m] == 0:
                    if len(outqueue[position[m]//timebetweenmachines-1]) > 0:
                        take_job = outqueue[position[m]//timebetweenmachines-1][0]
                        machine_load[m] = take_job
                        outqueue[position[m]//timebetweenmachines-1].remove(take_job)
        for p in range(0,production_machines):
            for s in range(0,pmachinesperstage[p]):
                if production_load[p][s] == 0:
                    if len(inqueue[p]) > 0:
                        next_job = inqueue[p][0]
                        counter = new_schedule_counter[p]
                        new_schedule[p][counter] = next_job
                        new_schedule_counter[p] += 1
                        production_load[p][s] = next_job
                        production_finish[p][s] = stopwatch+duration[p][next_job-1]
                        inqueue[p].remove(next_job)
    """
    Final display and return

    This function solely returns the makespan of a given schedule of startingtimes for
    a preselected amount of vehicles
    """
    #schedule.pop(production_machines)
    #print(new_schedule)
    return stopwatch

def main():
    #read_schedule(2,3,[4,2,1],3,[[0,0,1,0,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])
    #read_schedule(2,3,[4,2,1],3,[[0,1,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])
    #read_schedule(2,3,[4,2,1],3,[[1,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0]],8,2,[[1,2,3],[1,2,3],[1,3,2]],[[10,12,11],[5,6,7],[1,2,3]])
    print(fcfs(2, 10, [2, 2, 2, 2, 2, 2, 3, 2, 2, 2], 25, [[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]], 22, 2, [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]], [[1, 9, 5, 9, 7, 1, 6, 1, 4, 6, 6, 6, 6, 9, 4, 10, 6, 9, 3, 6, 3, 3, 9, 8, 6], [7, 2, 9, 3, 6, 3, 7, 10, 10, 7, 4, 1, 6, 4, 9, 8, 10, 10, 4, 7, 9, 8, 8, 4, 5], [7, 9, 9, 8, 5, 10, 8, 2, 9, 8, 10, 6, 2, 2, 1, 2, 8, 3, 3, 7, 3, 3, 3, 6, 3], [9, 2, 7, 10, 1, 7, 9, 4, 9, 3, 2, 7, 6, 8, 9, 4, 4, 10, 4, 1, 6, 9, 1, 8, 7], [7, 8, 7, 3, 10, 9, 9, 8, 10, 9, 3, 7, 5, 4, 3, 2, 7, 8, 7, 3, 4, 5, 9, 1, 4], [1, 1, 4, 2, 2, 2, 3, 10, 2, 10, 1, 1, 8, 3, 5, 10, 4, 4, 10, 2, 4, 6, 6, 1, 3], [2, 4, 6, 8, 6, 3, 5, 5, 8, 8, 6, 2, 10, 6, 9, 10, 6, 3, 3, 3, 5, 2, 7, 6, 5], [6, 10, 4, 3, 9, 8, 9, 7, 5, 3, 7, 5, 5, 2, 6, 3, 10, 7, 5, 3, 1, 9, 10, 2, 1], [4, 10, 4, 9, 4, 2, 7, 5, 2, 2, 3, 3, 10, 8, 3, 6, 3, 3, 2, 3, 8, 9, 8, 5, 4], [10, 3, 5, 5, 5, 10, 6, 4, 8, 7, 4, 6, 1, 7, 10, 7, 4, 1, 1, 6, 10, 4, 9, 7, 6]]
))

"""
[[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
   0.  0.  0.  1.]
 [ 0.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
   0.  0.  0.  0.]]
[[ 1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
   0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  1.  0.  0.  0.
   0.  0.  0.  0.]]
[[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
   0.  0.  0.  1.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  1.  0.  0.  0.  0.
   0.  0.  0.  0.]]
[[ 1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
   0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  1.  0.
   0.  0.  0.  0.]]
[[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
   0.  0.  0.  1.]
 [ 0.  0.  0.  0.  0.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
   0.  0.  0.  0.]]

"""

if __name__ == '__main__':
    main()
