"""
imports
"""
import numpy as np
import time
"""
Definitions of opening variables
"""
machines = 1
jobs = 3
production_machines = 3
startingtime = [[1,0,0,0,0,0,0,0]]
roundtime = 8
timebetweenmachines = 2
schedule = [[1,2,3],[1,2,3],[1,3,2]]
duration = [[10,12,11],[5,6,7],[1,2,3]]


x = 0                                               #variable showing the current time in the function (amount of time passed)
Finish_schedule = np.zeros(production_machines)         #binary matrix depicting whether a job on a machine has already been processed(1) or not(0)
inqueue = [[] for i in range(0,production_machines)]
outqueue = [[] for i in range(0,production_machines)]
machine_load = np.zeros(machines)                  #list showing the currently processed job on a machine (0 being none)
production_finish = np.zeros(production_machines) #list showing the finishing time of the current(last) processed job on a production machine
production_load = np.zeros(production_machines)   #list showing the currently processed job on a production machine (0 being none)
depot_out = jobs
depot_in = 0
depot_outqueue = []
startmachine = np.zeros(machines)

for i in range(0,jobs):
    depot_outqueue.append(i+1)

for m in range(0,machines):
    for l in range(0,roundtime):
        startmachine[m] += startingtime[m][l]*l

list_of_jobs = []
for i in range(0,jobs):
    list_of_jobs.append(i+1)
schedule.append(list_of_jobs)

starttime = time.time()

#while Finish_schedule[production_machines-1] < jobs:
while depot_in < 3:
#while time.time()-starttime<1:
#while x < 50:
    for m in range(0,machines):
        position = ((x-startmachine[m])%roundtime)/timebetweenmachines
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
        if production_load[p] > 0:
            if production_finish[p] <= x:
                outqueue[p].append(production_load[p])
                production_load[p] = 0
                Finish_schedule[p] += 1
        if production_load[p] == 0:
            if len(inqueue[p]) > 0:
                next_job = (schedule[p][int(Finish_schedule[p])])
                if next_job in inqueue[p]:
                    production_load[p] = next_job
                    production_finish[p] += duration[next_job-1][p]
                    inqueue[p].remove(next_job)
    print("Cmax = {}.".format(x))
    print("Finish:",Finish_schedule)
    print("Production:",production_load)
    print("Machines:",machine_load)
    print("inqueue",inqueue)
    print("outqueue",outqueue)
    print("depot_out:",depot_out)
    print("depot_in:",depot_in)
    x+=1
"""
print("Cmax = {}.".format(x))
print("Finish:",Finish_schedule)
print("Production:",production_load)
print("Machines:",machine_load)
print("depot_out:",depot_out)
print("depot_in:",depot_in)
"""
