import numpy as np
from toolbox.colored_messages import set_line
from natural_convection.flat_plate_ht import FlatPlateHT
from toolbox.constantes import __DIROUT__
import matplotlib.pyplot as plt


class FlatPlateHTAppli(object):
    """
    class to sweep with FSK with respect to beta parameter
    """
    def __init__(self, params):
        """
        class initialization
        """
        self.Prandtl = params["Prandtl"]

        # parameters for FalknerSkan class :
        self.eta_max = params["eta_max"]
        self.npt = params["npt"]
        self.method = params["method"]
        self.fsk = []

    def prandtl_sweep(self):
        """
        Sweeps over different Pr values
        """
        for value in self.Prandtl :
            s = FlatPlateHT(dict(eta_max=self.eta_max,
                                 npt=self.npt,
                                 Prandtl=value,
                                 method=self.method,
                                 grid=self.grid,
                                 verbose=False,
                                 plot=False
                                 ))
            s.solve()
            self.save_profiles(s)
            self.fsk.append(s.output)
    @staticmethod
    def save_profiles(case):
        """ Save in ascii format f, f', f'', v, d2u"""
        filename = __DIROUT__ + "flat_plate_pr_{:04d}.dat".format(int(case.Pr))
        print(filename)
        var = "#   eta            f              f'           f''            g           g'"
        header = "# Flat Plate Heat Transfer   \n" + var + "\n"
        with open(filename, 'w') as f:
            f.write(header)
            form = " {:12.5e} " * 6  + "\n"
            for k in range(len(case.eta)):
                f.write(form.format(case.eta[k], case.f[0, k], case.f[1, k], case.f[2,k], case.f[3,k],case.f[4,k]))
            f.close()

    def plot_profiles(self):
        """
        Plots the profiles of the swept Pr values
        :return:
        """
        fig, ax = plt.subplots(1, 2)
        fig.suptitle("Velocity and Temperature profiles")

        for case in self.Prandtl :
            filename = __DIROUT__ + "flat_plate_pr_{:04d}.dat".format(int(case))

            data = np.loadtxt(filename, skiprows=2)
            eta = data[:,0]
            f_prime = data[:,2]
            g = data[:,4]

            ax[0].plot(eta, f_prime,label=f"Pr={case}")
            ax[0].set_xlabel(r"$\eta$")
            ax[0].set_ylabel("f '")
            ax[0].grid(True)
            ax[0].legend()

            ax[1].plot(eta, g,label=f"Pr={case}")
            ax[1].set_xlabel(r"$\eta$")
            ax[1].set_ylabel("g")
            ax[1].grid(True)
            ax[1].legend()

        plt.show()





