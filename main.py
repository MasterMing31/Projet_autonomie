# -*- coding: utf-8 -*-
"""

@authors : MELNIC & MORAG
"""
import numpy as np
import matplotlib.pyplot as plt
from natural_convection.flat_plate_ht import FlatPlateHT
from natural_convection.flat_plate_ht_appli import FlatPlateHTAppli
from natural_convection.grx import Graphics
from toolbox.colored_messages import *

part = 1
task = 1

if part == 1:
    if task == 0:
        for a in [-1.5, -0.5, 0.0, 1, 3]:
            for Pr in [0.5, 1, 3, 5, 8, 10]:
                parameters = dict(eta_max=15,
                                npt=201,
                                Prandtl=Pr,
                                a=a,
                                X=1,
                                Hartman=0,
                                Eckert=0,
                                Grashof=0,
                                Lambda=0,
                                Reynolds=1,
                                method=1,
                                grid="geometric",
                                verbose=False,
                                plot=False,
                                case = 1,
                                f2_f4_init_guess = [-1.4, -0.5],
                                M=0
                                )
                s = FlatPlateHT(parameters)
                s.solve()
        set_info("normal end of execution")
    
    elif task == 1:
        g = Graphics(case=1, M=0)
        g.run(task=1)
        set_info("normal end of execution")

elif part == 2:
    if task == 0:
        for M in [0, 1, 3, 5, 8, 10]:
            parameters = dict(eta_max=7.1,
                            npt=201,
                            Prandtl=1,
                            a=-1.5,
                            X=1.5,
                            Hartman=np.sqrt(M),
                            Eckert=0.1,
                            Grashof=2,
                            Lambda=0.1,
                            Reynolds=1,
                            method=1,
                            grid="geometric",
                            verbose=False,
                            plot=False,
                            case = 2,
                            f2_f4_init_guess = [-1.14, 1.],
                            M = M
                            )
            s = FlatPlateHT(parameters)
            s.solve()
        set_info("normal end of execution")
    
    elif task == 1:
        g = Graphics(case=2, M=0)
        g.run(task=2)
        plt.show()
        set_info("normal end of execution")

elif part == 3:
    if task == 1:
        for a in [1, 5, 8]:
            parameters = dict(eta_max=15,
                        npt=201,
                        Prandtl=1,
                        a=a,
                        X=1.5,
                        Hartman=None,
                        Eckert=0,
                        Grashof=0,
                        Lambda=0,
                        Reynolds=1,
                        method=1,
                        grid="geometric",
                        verbose=False,
                        plot=True,
                        case = 3,
                        f2_f4_init_guess = [-1.14, 1.],
                        M = 0.5 # Ha^2/Re
                        )
            s = FlatPlateHT(parameters)
            s.solve()
        set_info("normal end of execution")
    
    elif task == 1:
        g = Graphics(case=3, M=0)
        g.run(task=2)
        plt.show()
        set_info("normal end of execution")

        































































def task_0():
    """
    Optimization of the initial guesses for f''(0) and g'(0). The sweep starts from Pr = 1 and goes up to Pr = 10.
    It saves the results in a .dat file.
    This task takes a lot of time to compute. For later tasks use data from the file.

    """
    for a in [-1.5, -0.5, 0.0, 1, 3]:
         for Pr in [0.5, 1, 3, 5, 8, 10]:
            parameters = dict(eta_max=15,
                            npt=201,
                            Prandtl=Pr,
                            a=a,
                            X=1,
                            Hartman=0,
                            Eckert=0,
                            Grashof=0,
                            Lambda=0,
                            Reynolds=1,
                            method=1,
                            grid="geometric",
                            verbose=False,
                            plot=False,
                            case = 1
                            )
            s = FlatPlateHT(parameters)
            s.solve()

    # parameters = dict(eta_max=15,
    #                npt=201,
    #                Prandtl=0.5,
    #                a=-1.5,
    #                X=1,
    #                Hartman=0,
    #                Eckert=0,
    #                Grashof=0,
    #                Lambda=0,
    #                Reynolds=1,
    #                method=1,
    #                grid="geometric",
    #                verbose=False,
    #                plot=False
    #                )
    # s = FlatPlateHT(parameters)
    # s.solve()
 
    set_info("normal end of execution")

def task_1():
    """
    Computation of the velocity and temperature profiles around a flat plate for a single Pr value .
    """
    parameters = dict(eta_max=15,
                   npt=201,
                   Prandtl=0.5,
                   a=-1.5,
                   X=1,
                   Hartman=0,
                   Eckert=0,
                   Grashof=0,
                   Lambda=0,
                   Reynolds=1,
                   method=1,
                   grid="geometric",
                   verbose=False,
                   plot=False,
                   case = 1,
                   f2_f4_init_guess = [-1.14, 1.],
                   M=0
                   )
    s = FlatPlateHT(parameters)
    set_info("normal end of execution")

def task_2():
    """
    Post processing of the results 
    """
    g = Graphics(case=1, M=0)
    g.run(task=1)
    set_info("normal end of execution")

def task_3():
    """
    Run simulation for case 2
    """
    parameters = dict(eta_max=7.1,
                   npt=201,
                   Prandtl=1,
                   a=-1.5,
                   X=1.5,
                   Hartman=1,
                   Eckert=0.1,
                   Grashof=2,
                   Lambda=0.1,
                   Reynolds=1,
                   method=1,
                   grid="geometric",
                   verbose=False,
                   plot=True,
                   case = 2,
                   f2_f4_init_guess = [-1.14, 1.],
                   M = 0
                   )
    s = FlatPlateHT(parameters)
    s.solve()
    print(s.f2_f4_init)
    g = Graphics(case=2, M=s.M)
    g.run(task=2)
    set_info("normal end of execution")


task = None

task_dispatch = {0: task_0, # run simulation to generate initial guesses data
                 1: task_1, # post processing table
                 2: task_2, # post processing plots
                 3: task_3} # run simulation for case 2
task_dispatch.get(task, lambda: print("Invalid task"))()

