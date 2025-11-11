from scipy import optimize, integrate
import numpy as np
import matplotlib.pyplot as plt
import glob
from toolbox.colored_messages import *
from toolbox.constantes import __DIROUT__
from toolbox.constantes import __DIR__
from toolbox.tools import set_data_from_file, load_data
import os
from tabulate import tabulate


class FlatPlateMHD(object):
    """
    solves the heat transfer around a flat plate for different Prandtl numbers

    """

    def __init__(self, par):
        """
        class initialization
        """
        method_available = ("BDF", "RK45", "RK23", "DOP853", "LSODA")
        self.eta_max = par['eta_max']
        self.grid = par["grid"]
        self.npt = par["npt"]
        self.Pr = par["Prandtl"]
        self.a = par["a"]
        self.X = par["X"]
        self.Ec = par["Eckert"]
        self.Gr = par["Grashof"]
        self.lbda = par["Lambda"]
        self.case = par["case"]
        self.M = par["M"]

        if par["method"] >= 5:
            raise ValueError("parameter 'method'  must be lower than  5")
        self.method = method_available[par["method"]]
        self.verbose = par["verbose"]
        self.plot = par["plot"]

        self.f2_f4_init_guess = np.array(par["f2_f4_init_guess"]) 

        self.eta = None
        self.f = None
        self.f2_f4_init = None
        self.deta_min = 0
        self.output = None

    def set_grid(self):
        """
        grid
        """
        self.eta = np.linspace(0, self.eta_max, self.npt)
        self.deta_min = self.eta[1] - self.eta[0]

    def guess_optimization(self):
        self.set_grid()

        result = optimize.minimize(fun=self.error_squared, x0=self.f2_f4_init_guess,
                                   method='Nelder-Mead', options={'fatol': 1e-18})

        self.f2_f4_init = result.x

        if self.verbose:
            print("f''_init     : %f" % self.f2_f4_init)
            print("Residual     : %e" % result.fun)

    def solve(self):
        """
        Solves the heat transfer around a flat plate by using the Nelder-Mead simplex optimization algorithm

        """
        self.guess_optimization()

        # Calculate the final solution
        self.eta, self.f = self.solution(self.f2_f4_init)
        if self.case == 1:
            self.save_profiles(filename=__DIROUT__ + f"case_1_a={self.a}_Pr={self.Pr}.dat")
        elif self.case == 2:
            self.save_profiles(filename=__DIROUT__ + f"case_2_HaRe={self.M}.dat")
        elif self.case == 3:
            self.save_profiles(filename=__DIROUT__ + f"case_3_a={self.a}.dat")
        elif self.case == 4:
            self.save_profiles(filename=__DIROUT__ + f"case_4_X={self.X}.dat")




        # self.set_characteristics(self.eta, self.f)
        # self.get_characteristics()
            
        
        # if self.plot:
        #     self.display_profiles()
        #     self.save_profiles()


    def error_squared(self, f2_f4_init):
        """
        Computes the error squared used later for the optimization
        """

        self.eta, self.f = self.solution(f2_f4_init)
        error_squared = self.f[1, -1]**2 + self.f[3, -1]**2

        return error_squared

    def solution(self, f2_f4_init):
        """
        Gets the solution of the ODE
        """
        f_init = np.array([0, 1, float(f2_f4_init[0]), 1, float(f2_f4_init[1])], dtype=object)  # f(0), f'(0), f''(0), g(0) and g'(0)
        sol = integrate.solve_ivp(self.ode, t_span=(0, self.eta[-1]), t_eval=self.eta, y0=f_init, method=self.method, rtol=1e-9, atol=1e-12)

        return sol.t, sol.y   

    def ode(self, eta, f):
        """

        """
        df_deta = np.zeros(5, dtype=float)
        df_deta[0] = f[1]
        df_deta[1] = f[2]
        df_deta[2] = -f[0]*f[2] +2*f[1]**2 - 2*self.M * np.exp(-self.X) * f[1] + 2*self.Gr*np.exp((self.a/2 - 2)*self.X) * f[3]
        df_deta[3] = f[4]
        df_deta[4] = self.Pr * (
            -f[0]*f[4] 
            + self.a*f[1]*f[3] 
            - np.exp(self.X*(1-self.a/2)) * self.Ec*(2*self.M * f[1]**2 + f[2]**2*np.exp(self.X)) 
            - 2 * self.lbda * np.exp(-self.X) * f[3])

        return df_deta


    def set_characteristics(self, eta, sol):
        """
        boundary layer characteristics
        """
        df = sol[1, :]
        theta = sol[3, :]

        # --- Couche limite de vitesse (f' → 0)
        u_max = np.max(self.f[1, :])
        self.i_vbl = np.argmin(abs(self.f[1, :] - 0.01 * u_max))
        delta_m = self.eta[self.i_vbl]

        # --- Couche limite thermique (θ → 0)
        self.i_tbl = np.argmin(abs(self.f[3, :]))   # θ tend vers 0 à l'infini
        delta_t = self.eta[self.i_tbl]

        self.Cf_Rex = np.sqrt(2 * self.X) * self.f[2, 0]
        self.Nux_Rex = -np.sqrt(self.X / 2) * self.f[4, 0]
        self.output_tab = [self.a, 
                           self.Pr, 
                           self.Cf_Rex, 
                           self.Nux_Rex, 
                           delta_m, 
                           delta_t,
                           ]

    def get_characteristics(self):
        """
        boundary layer characteristic: display
        """
        set_line()
        set_table("Boundary layer characteristics")
        headers = ["a", "Pr", 
                   "Cf/2 * sqrt(Re_x)", 
                   "Nu_x / sqrt(Re_x)", 
                   "delta_m", "delta_t", 
                   ""]
        self.output_tab = ["{:.4f}".format(x) for x in self.output_tab]
        print(tabulate([self.output_tab], headers=headers, tablefmt="fancy_grid"))
        set_line()


    def display_profiles(self):
        """
        show the results of the ODE
        """
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.suptitle(f"Velocity and Temperature profiles (Pr = {self.Pr})")
        ax.plot(self.eta, self.f[1, :])
        ax.set_xlabel(r"$\eta$")
        ax.set_ylabel("f '")
        ax.grid()

        # ax[1].plot(self.eta, self.f[3, :])
        # ax[1].set_xlabel(r"$\eta$")
        # ax[1].set_ylabel("g")
        # ax[1].grid()
        plt.show()

    def save_profiles(self, filename):
        """ Save in ascii format f, f', f'', theta, dtheta"""
        print(filename)
        var = "#	   eta            f              f'           f''          theta         dtheta"
        header = ("#  Mixed convection heat transfer in the boundary \
                  layers on an exponentially stretching surface"
                  " with magnetic field   \n") + var + "\n"
        with open(filename, 'w') as f:
            f.write(header)
            form = " {:12.5e} " * 6  + "\n"
            for k in range(len(self.eta)):
                f.write(form.format(self.eta[k], 
                                    self.f[0, k], 
                                    self.f[1, k], 
                                    self.f[2,k], 
                                    self.f[3,k],
                                    self.f[4,k]))
            f.close()



























    def initial_guess(self):
         """
         Proceeds to do a sweep over different Pr values in order to find the right initial guesses for f''(0) and g'(0)

         """
         filename = __DIROUT__ + "flat_plate_guesses_{:01d}.dat".format(1)
         print(filename)
         var = "#     Pr           f''(0)         g'(0)"
         header = "# Flat Plate Heat Transfer initial guesses  \n" + var + "\n"
         with open(filename, 'w') as f:
             f.write(header)
             form = " {:12.5e} " * 3 + "\n"

             for i, Pr_value in range(1, 11):
                 self.Pr = Pr_value
                 self.solve()
                 new_guess = [self.f[2,0], self.f[4,0]]
                 f.write(form.format(self.Pr, self.f[2, 0], self.f[4, 0]))
                 f.flush()
                 self.f2_f4_init_guess = new_guess
             f.close()