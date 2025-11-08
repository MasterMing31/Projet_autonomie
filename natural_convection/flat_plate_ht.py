from scipy import optimize, integrate
import numpy as np
import matplotlib.pyplot as plt
from toolbox.colored_messages import *
from toolbox.constantes import __DIROUT__
from toolbox.constantes import __DIR__
import os


class FlatPlateHT(object):
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
        self.Ha = par["Hartman"]
        self.Ec = par["Eckert"]
        self.Gr = par["Grashof"]
        self.lbda = par["Lambda"]
        self.Re = par["Reynolds"]

        if par["method"] >= 5:
            raise ValueError("parameter 'method'  must be lower than  5")
        self.method = method_available[par["method"]]
        self.verbose = par["verbose"]
        self.plot = par["plot"]

        filename = "flat_plate_guesses_1.dat"
        script_dir = os.path.dirname(__file__)
        src_dir = os.path.dirname(script_dir)
        data_dir = os.path.join(src_dir, "data")
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path):
            data = np.loadtxt(file_path, skiprows=2)
            prandtl_list = data[:, 0]
            df2, dg = None, None

            for i in range(len(prandtl_list)):
                if float(self.Pr) == prandtl_list[i]:
                    df2 = data[i, 1]
                    dg = data[i, 2]

            self.f2_f4_init_guess = np.array([df2, dg])
        else:
            self.f2_f4_init_guess = np.array([-1.30021114, -0.64689448])

        self.ratio = 10.            # to set the minimum step for a geometric grid
        # variables declaration
        self.eta = None
        self.f = None
        self.f2_f4_init = None
        self.deta_min = 0
        self.output = None


    def set_grid(self):
        """
        grid
        """
        if self.grid == "geometric":
            self.deta_min = self.eta_max / (self.ratio * (self.npt - 1))
            self.eta = np.hstack((0, np.geomspace(self.deta_min, self.eta_max, self.npt-1)))
            self.eta[-1] = self.eta_max   # necessary because of the round-off error
        else:
            self.eta = np.linspace(0, self.eta_max, self.npt)
            self.deta_min = self.eta[1] - self.eta[0]

    def guess_optimization(self):
        self.set_grid()

        result = optimize.minimize(fun=self.error_squared, x0=self.f2_f4_init_guess,
                                   method='nelder-mead', options={'fatol': 1e-12})

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
        print(self.eta[-1])
        if self.plot:
            self.display_profiles()
            self.save_profiles()


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
        f_init = np.array([0, 1, float(f2_f4_init[0]), 1, float(f2_f4_init[1])], dtype=object)  # f(0), f'(0), f''(0),g(0) and g'(0)
        sol = integrate.solve_ivp(self.ode, t_span=(self.eta[0], self.eta[-1]), t_eval=self.eta, y0=f_init, method=self.method)

        return sol.t, sol.y   

    def ode(self, eta, f):
        """

        """
        df_deta = np.zeros(5, dtype=float)
        df_deta[0] = f[1]
        df_deta[1] = f[2]
        df_deta[2] = -f[0]*f[2] +2*f[1]**2 - 2*(self.Ha**2)/self.Re * np.exp(-self.X) * f[1] + 2*self.Gr*np.exp((self.a/2 - 2)*self.X) * f[3]
        df_deta[3] = f[4]
        df_deta[4] = self.Pr * (
            -f[0]*f[4] 
            + self.a*f[1]*f[3] 
            - np.exp(self.X*(1-self.a/2)) * self.Ec*(2*self.Ha**2/self.Re * f[1]**2 + f[2]**2*np.exp(self.X)) 
            - 2 * self.lbda * np.exp(-self.X) * f[3])

        return df_deta

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
                 new_guess = [self.f[2,0],self.f[4,0]]
                 f.write(form.format(self.Pr, self.f[2, 0], self.f[4, 0]))
                 f.flush()
                 self.f2_f4_init_guess = new_guess
             f.close()


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

    def save_profiles(self):
        """ Save in ascii format f, f', f'', theta, dtheta"""
        filename = __DIROUT__ + "profile_{:01f}.dat".format(self.Pr)
        print(filename)
        var = "#	   eta            f              f'           f''          theta         dtheta"
        header = ("#  Mixed convection heat transfer in the boundary layers on an exponentially stretching surface"
                  " with magnetic field   \n") + var + "\n"
        with open(filename, 'w') as f:
            f.write(header)
            form = " {:12.5e} " * 6  + "\n"
            for k in range(len(self.eta)):
                f.write(form.format(self.eta[k], self.f[0, k], self.f[1, k], self.f[2,k], self.f[3,k],
                                    self.f[4,k]))
            f.close()
