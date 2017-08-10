#!/usr/bin/env python3
"""
Selfwritten unittest for the heuristic and the calculator of the makespan for
a given schedule

This unittest tests the functions calc_profit and get_solution for their
functionality and special cases with 0 as input
"""
import unittest
from heuristic import heuristic
from readschedule import read_input, read_schedule
import numpy as np


class TestHeuristic(unittest.TestCase):
    def setUp(self):
        self.maxmachines1 = 1
        self.maxmachines2 = 8
        self.production_machines1 = 2
        self.production_machines2 = 10
        self.pmachinesperstage1 = [1,1]
        self.pmachinesperstage2 = [read_input("pmachinesperstage.txt")][0]
        self.jobs1 = 4
        self.jobs2 = 25
        self.roundtime1 = 6
        self.roundtime2 = 22
        self.timebetweenmachines = 2
        self.schedule1 = [[1,2,3,4],[1,2,3,4]]
        self.schedule2 = [read_input("pschedule.txt")][0]
        self.duration1 = [[8,4,5,3],[6,10,5,6]]
        self.duration2 = [read_input("ptime.txt")][0]
        self.iterations1 = 1
        self.iterations2 = 10
        self.sequence1 = [[1,0,0,0,0,0]]
        self.sequence2 = [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],]


    def test_heuristic_simple(self):
        self.assertEqual(read_schedule(self.maxmachines1,self.production_machines1,self.pmachinesperstage1,
                self.jobs1,self.sequence1,self.roundtime1,self.timebetweenmachines,self.schedule1,
                self.duration1),48)
        self.assertTrue(heuristic(self.maxmachines1,self.production_machines1,self.pmachinesperstage1,
                self.jobs1,self.roundtime1,self.timebetweenmachines,self.schedule1,self.duration1,
                self.iterations1),list)

    def test_heuristic_adv(self):
        self.assertEqual(read_schedule(self.maxmachines2,self.production_machines2,self.pmachinesperstage2,
                self.jobs2,self.sequence2,self.roundtime2,self.timebetweenmachines,self.schedule2,
                self.duration2),199)
        self.assertTrue(heuristic(self.maxmachines2,self.production_machines2,self.pmachinesperstage2,
                self.jobs2,self.roundtime2,self.timebetweenmachines,self.schedule2,self.duration2,
                self.iterations2),list)
if __name__ == '__main__':
    unittest.main(verbosity=2)
