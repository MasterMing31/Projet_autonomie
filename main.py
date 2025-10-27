# -*- coding: utf-8 -*-
"""
Résolution de l'équation de Falkner-Skan-Cooke

Christophe Airiau, August 2022

Version pour les étudiants: september, 17 th, 2023
"""

import matplotlib.pyplot as plt
from natural_convection.flat_plate_ht import FlatPlateHT
from natural_convection.flat_plate_ht_appli import FlatPlateHTAppli
from toolbox.colored_messages import *

def task_0():
    """
    Optimization of the initial guesses for f''(0) and g'(0). The sweep starts from Pr = 1 and goes up to Pr = 10.
    It saves the results in a .dat file.
    This task takes a lot of time to compute. For later tasks use data from the file.

    """
    parameters = dict(eta_max=7,
                   npt=201,
                   Prandtl=1,a=0,X=1,Hartman=0,Eckert=0,Grashof=0,Lambda=0,Reynolds=1,
                   method=1,
                   grid="geometric",
                   verbose=False,
                   plot=True
                   )
    s = FlatPlateHT(parameters)
    s.solve()
    
    set_info("normal end of execution")

def task_1():
    """
    Computation of the velocity and temperature profiles around a flat plate for a single Pr value .
    """
    parameters = dict(eta_max=20,
                   npt=201,
                   Prandtl=10,
                   method=1,
                   verbose=False,
                   plot=False
                   )
    s = FlatPlateHT(parameters)
    print(f"Initial_guesses : {s.f2_f4_init_guess} ")
    s.solve()
    s.display_profiles()

    set_info("normal end of execution")

def task_2():
    """
    Study of the Falkner-Skan solution for different beta values.
    :return:
    """
    parameters = dict(eta_max=20,
                   npt=201,
                   Prandtl=[1.0,7.0,10],
                   method=1,
                   verbose=False,
                   plot=False
                   )
    s = FlatPlateHTAppli(parameters)
    s.prandtl_sweep()# launch of the sweep through different Prandtl values
    s.plot_profiles()
    set_info("normal end of execution")


task_dispatch = {0: task_0,
                 1: task_1,
                 2: task_2}
task = 0
task_dispatch.get(task, lambda: print("Invalid task"))()
