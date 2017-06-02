#!/usr/bin/env python3

def generateptime(production_machines, jobs):
    from random import randint

    duration = []
    machineduration = []
    for i in range(production_machines):
        for j in range(jobs):
            machineduration.append(randint(1,10))
        duration.append(machineduration)
        machineduration = []

    return duration

def generateschedule(production_machines, jobs):

    schedule = []
    machineschedule = []
    for i in range(production_machines):
        for j in range(jobs):
            machineschedule.append(j+1)
        schedule.append(machineschedule)
        machineschedule = []

    return schedule

def main():
    file = open("ptime.txt","w")
    file.write(str(generateptime(10,25)))
    file = open("pschedule.txt","w")
    file.write(str(generateschedule(10,25)))

if __name__ == '__main__':
    main()
