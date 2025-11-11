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
                                Eckert=0,
                                Grashof=0,
                                Lambda=0,
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
                            Eckert=0.1,
                            Grashof=2,
                            Lambda=0.1,
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
    if task == 0:
        for a in [1, 5, 8]:
            parameters = dict(eta_max=15,
                        npt=201,
                        Prandtl=1,
                        a=a,
                        X=1.5,
                        Hartman=None,
                        Grashof=2,
                        Lambda=0.1,
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

elif part == 4:
    if task == 0:
        for X in [0.1, 1, 5]:
            parameters = dict(eta_max=15,
                        npt=201,
                        Prandtl=1,
                        a=2,
                        X=X,
                        Eckert=0.1,
                        Grashof=2,
                        Lambda=0.1,
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

