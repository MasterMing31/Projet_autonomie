"""
Post processing functions for natural convection over a flat plate.
@authors : MELNIC & MORAG
"""

import glob
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns
from tabulate import tabulate
from toolbox.colored_messages import set_title, set_msg, set_alert, set_section, set_table
from toolbox.tools import load_data, set_data_from_file
from toolbox.constantes import __DIR__, __FIGSIZE__, __FS__, __LS__, \
                               __COMPONENTS__, __VARS__, __DIROUT__ 


class Graphics(object):
    """
    new class to make nice plots
    """
    def __init__(self, case):
        """ initialisation """
        self.case = case
        if case == 1:
            self.filename = __DIROUT__ + "case_1_a=-0.5_Pr=0.5.dat"
        elif case == 2:
            # self.filename = __DIROUT__ + f"case_2_HaRe={M}.dat"
            self.files = glob.glob(os.path.join(__DIROUT__, "case_2_HaRe=*"))
        # self.plot_options = plot_options

        
        # self.files = ["cf_positive_beta.dat", "cf_negative_beta.dat"]
        # for f in self.files:
        # self.filename.append(__DIR__ + f)
        self.data = None
        self.beta_ref = []
        self.profiles_list = None
        self.dict_profiles = None
        self.eta = None
        self.plot_params = None
        self.index_beta = []
        
        # self.initiate_plot_params()

    def run(self, task=2):
        """ main method"""
        # self.data = load_data(self.filename, skiprows=2, vb=True)
        if task == 1:
            self.table_dtheta0()
            self.table_d2f0()
            pass
        elif task == 2:
            self.plots_df()
            self.plots_dtheta()
        # elif task == 3:
        # elif task == 4:
  
        else:
            set_alert("task parameter must be in (1, 2, 3, 4)")

    def table_dtheta0(self, directory=__DIROUT__):
        """
        Crée un tableau à double entrée des premières valeurs de dtheta
        selon a (lignes) et Pr (colonnes), et l'affiche avec tabulate.
        """
        files = glob.glob(directory + "case_1_profile_a=*Pr=*.dat")
        data = []
        set_table("dtheta(0) values for case 1")
        for file in files:
            try:
                basename = file.split("/")[-1]
                a_str = basename.split("_a=")[1].split("_Pr=")[0]
                Pr_str = basename.split("_Pr=")[1].split(".dat")[0]
                a = float(a_str)
                Pr = float(Pr_str)
            except Exception as e:
                print(f"Erreur lecture nom fichier {file} : {e}")
                continue

            with open(file, "r") as f:
                lines = [l for l in f if not l.strip().startswith("#")]
            if not lines:
                continue
            try:
                dtheta0 = float(lines[0].split()[-1])
                data.append((a, Pr, dtheta0))
            except Exception as e:
                print(f"Erreur lecture données dans {file} : {e}")
                continue

        if not data:
            print("Aucun fichier valide trouvé.")
            return

        data = np.array(data)
        a_values = np.unique(data[:, 0])
        Pr_values = np.unique(data[:, 1])

        table = np.full((len(a_values), len(Pr_values)), np.nan)

        for a, Pr, dtheta0 in data:
            i = np.where(a_values == a)[0][0]
            j = np.where(Pr_values == Pr)[0][0]
            table[i, j] = dtheta0

        headers = ["a \\ Pr"] + [f"{Pr:.2f}" for Pr in Pr_values]
        rows = [[f"{a:.2f}"] + [f"{val:.4e}" if not np.isnan(val) else "-" for val in row] 
                for a, row in zip(a_values, table)]

        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        return a_values, Pr_values, table
    
    def table_d2f0(self, directory=__DIROUT__):
        """
        Crée un tableau à double entrée des premières valeurs de dtheta
        selon a (lignes) et Pr (colonnes), et l'affiche avec tabulate.
        """
        files = glob.glob(directory + "case_1_profile_a=*Pr=*.dat")
        data = []
        set_table("f''(0) values for case 1")
        for file in files:
            try:
                basename = file.split("/")[-1]
                a_str = basename.split("_a=")[1].split("_Pr=")[0]
                Pr_str = basename.split("_Pr=")[1].split(".dat")[0]
                a = float(a_str)
                Pr = float(Pr_str)
            except Exception as e:
                print(f"Erreur lecture nom fichier {file} : {e}")
                continue

            with open(file, "r") as f:
                lines = [l for l in f if not l.strip().startswith("#")]
            if not lines:
                continue
            try:
                dtheta0 = float(lines[0].split()[3])
                data.append((a, Pr, dtheta0))
            except Exception as e:
                print(f"Erreur lecture données dans {file} : {e}")
                continue

        if not data:
            print("Aucun fichier valide trouvé.")
            return

        data = np.array(data)
        a_values = np.unique(data[:, 0])
        Pr_values = np.unique(data[:, 1])

        table = np.full((len(a_values), len(Pr_values)), np.nan)

        for a, Pr, d2f0 in data:
            i = np.where(a_values == a)[0][0]
            j = np.where(Pr_values == Pr)[0][0]
            table[i, j] = d2f0

        headers = ["a \\ Pr"] + [f"{Pr:.2f}" for Pr in Pr_values]
        rows = [[f"{a:.2f}"] + [f"{val:.4e}" if not np.isnan(val) else "-" for val in row] 
                for a, row in zip(a_values, table)]

        print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
        return a_values, Pr_values, table

    def plots_df(self):
        """
        make plots
        """
        data = []
        for file in self.files:
            if self.case == 2:
                M_str = file.split('=')[1].replace('.dat', '')   
                M = float(M_str)
                label = f"$Ha²/Re = {M}$"
            elif self.case == 3:
                a_str = file.split('=')[1].replace('.dat', '')   
                a = float(a_str)
                label = f"$a = {a}$"
            elif self.case == 4:
                X_str = file.split('=')[1].replace('.dat', '')   
                X = float(X_str)
                label = f"$X = {X}$"

            data = set_data_from_file(file, skiprows=2, vb=False)
            plt.plot(data[0][:], data[2][:], label=label)

        plt.xlabel(r'$\eta$')
        plt.ylabel(r"$f'$", rotation=0)
        plt.title(r"Temperature profile $\theta$ vs $\eta$")
        plt.grid()
        plt.legend()
        plt.show()

    def plots_dtheta(self):
        """
        make plots
        """
        data = []
        for file in self.files:
            if self.case == 2:
                M_str = file.split('=')[1].replace('.dat', '')   
                M = float(M_str)
                label = f"$Ha²/Re = {M}$"
            elif self.case == 3:
                a_str = file.split('=')[1].replace('.dat', '')   
                a = float(a_str)
                label = f"$a = {a}$"
            elif self.case == 4:
                X_str = file.split('=')[1].replace('.dat', '')   
                X = float(X_str)
                label = f"$X = {X}$"

            data = set_data_from_file(file, skiprows=2, vb=False)
            plt.plot(data[0][:], data[4][:], label=label)

        plt.xlabel(r'$\eta$')
        plt.ylabel(r"$\theta$", rotation=0)
        plt.title(r"Temperature profile $\theta$ vs $\eta$")
        plt.grid()
        plt.legend()
        plt.show()