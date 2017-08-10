#!/usr/bin/env python3
from readschedule import read_schedule

def read_input_duration(inputfile):
    import ast
    duration = []
    with open(inputfile) as data:
        duration = ast.literal_eval(data.read())
    return duration

def read_input_schedule(inputfile):
    import ast
    schedule = []
    with open(inputfile) as data:
        schedule = ast.literal_eval(data.read())
    return schedule

def pmachinesperstage_func(duration):
    avgmachine = sum(sum(element for element in duration[index]) for index in range(len(duration)))/len(duration)
    pmachinesperstage = []
    for i in range(len(duration)):
        machinesum = 0
        for j in range(len(duration[0])):
            machinesum += duration[i][j]
        avg = machinesum
        if avg/avgmachine < 0.8:
            pmachinesperstage.append(1)
        elif avg/avgmachine < 1.2:
            pmachinesperstage.append(2)
        elif avg/avgmachine < 1.3:
            pmachinesperstage.append(3)
        else:
            pmachinesperstage.append(4)
    return pmachinesperstage

if __name__ == '__main__':
    duration = [read_input_duration("ptime.txt")][0]
    file = open("pmachinesperstage.txt","w")
    file.write(str(pmachinesperstage_func(duration)))
