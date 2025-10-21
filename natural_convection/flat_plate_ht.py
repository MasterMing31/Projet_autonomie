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
        self.npt = par["npt"]
        self.Pr = par["Prandtl"]
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
            self.f2_f4_init_guess = np.array([1, -1])

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

        self.eta = np.linspace(0, self.eta_max, self.npt)
        self.deta_min = self.eta[1] - self.eta[0]

    def solve(self):
        """
        Solves the heat transfer around a flat plate by using the Nelder-Mead simplex optimization algorithm

        """
        self.set_grid()

        result = optimize.minimize(fun=self.error_squared, x0=self.f2_f4_init_guess,
                                   method='nelder-mead', options={'fatol': 1e-12})

        self.f2_f4_init = result.x

        if self.verbose:
            print("f''_init     : %f" % self.f2_f4_init)
            print("Residual     : %e" % result.fun)

        # Calculate the final solution
        self.eta, self.f = self.solution(self.f2_f4_init)
        if self.plot:
            self.display_profiles()


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
        Ha = 0
        Re = 1
        Gr = 0
        Ec = 0
        X = 1
        a = -0.5
        lambd = 0

        df_deta = np.zeros(5, dtype=float)
        df_deta[0] = f[1]
        df_deta[1] = f[2]
        df_deta[2] = -f[0]*f[2] +2*f[1]**2 - 2*(Ha**2)/Re * np.exp(-X) * f[1] + 2*Gr*np.exp((a/2 - 2)*X) * f[3]
        df_deta[3] = f[4]
        df_deta[4] = self.Pr * (-f[0]*f[4] + a*f[1]*f[3] -np.exp(X*(1-a/2)) * Ec*(2*Ha**2/Re * f[1]**2 + f[2]**2*np.exp(X)) - 2 * lambd * np.exp(-X) * f[3])

        return df_deta

    # def initial_guess(self):
    #     """
    #     Proceeds to do a sweep over different Pr values in order to find the right initial guesses for f''(0) and g'(0)

    #     """
    #     filename = __DIROUT__ + "flat_plate_guesses_{:01d}.dat".format(1)
    #     print(filename)
    #     var = "#     Pr           f''(0)         g'(0)"
    #     header = "# Flat Plate Heat Transfer initial guesses  \n" + var + "\n"
    #     with open(filename, 'w') as f:
    #         f.write(header)
    #         form = " {:12.5e} " * 3 + "\n"

    #         for i, Pr_value in range(1, 11):
    #             self.Pr = Pr_value
    #             self.solve()
    #             new_guess = [self.f[2,0],self.f[4,0]]
    #             f.write(form.format(self.Pr, self.f[2, 0], self.f[4, 0]))
    #             f.flush()
    #             self.f2_f4_init_guess = new_guess
    #         f.close()


    def display_profiles(self):
        """
        show the results of the ODE
        """
        fig, ax = plt.subplots(1, 2,figsize=(8, 7))
        fig.suptitle(f"Velocity and Temperature profiles (Pr = {self.Pr})")
        ax[0].plot(self.eta, self.f[1, :])
        ax[0].set_xlabel(r"$\eta$")
        ax[0].set_ylabel("f '")
        ax[0].grid()

        ax[1].plot(self.eta, self.f[3, :])
        ax[1].set_xlabel(r"$\eta$")
        ax[1].set_ylabel("g")
        ax[1].grid()
        plt.show()