"""
Created on Tue May  1 13:52:07 2018

@author: florent
"""

from base_functions import *

figsize = (6, 4)

do_legend = 1
Nlinspace = 10000
min_s, max_s = 0.2, 0.8
a = 0.0
b = 3.0
my_model = 1

do_save = 1

do_test = 0
factor_test = 10 if do_test else 100




def Total_Cov(model, n, p, T):
    if model == 0:
        Z = np.matrix(np.random.randn(n + p, T))
        return ([0] * n, Z * (Z.T) / T)
    else:
        Ech = []
        for i in range(n):
            Ech.append(the_fancy_ran_var())
        Ech = sorted(Ech, reverse=1)
        C = np.bmat([np.diag(Ech), np.zeros((n, p - n))]) if n != p else np.diag(Ech)
        Sitrue = np.bmat([[np.eye(n), C], [C.T, np.eye(p)]])
        return (Ech, Empirical_Covariance(T, Sitrue))


def histo(E, ax, color="b", reg_coeff=1, label="", linewidth=1):
    if label == "":
        ax.hist(
            E,
            bins=int(round(reg_coeff * len(E) ** 0.416 + 2)),
            density=True,
            histtype="step",
            color=color,
            linewidth=linewidth,
        )
    else:
        ax.hist(
            E,
            bins=int(round(reg_coeff * len(E) ** 0.416 + 2)),
            density=True,
            histtype="step",
            color=color,
            label=label,
            linewidth=linewidth,
        )

sv_labels={'empirical': '$s_k$ (empirical sing. val.)',
           'cleaned': '$s_k^{\mathrm{clean}}$ (cleaned sing. val.)',
           'true': '$s_k^{\mathrm{true}}$ (true sing. val.)'}

def plot_results(my_model, True_s, Emp_Sing_Val, Clean_Sing_Val, RIE_flag, file_name,
                 dimension_details,
                 figsize=figsize):
    fig, ax = plt.subplots(figsize=figsize, tight_layout=True)
    min_s, max_s = 0.2, 0.8
    if RIE_flag == 0:
        # plt.figure()
        if my_model == 0:
            ax.axvline(
                x=0,
                linestyle="--",
                color="r",
                linewidth=3,
                label=sv_labels['true'],
            )
        else:
            x = np.linspace(min_s, max_s, Nlinspace)
            y = the_final_fancy_density(x)
            ax.plot(
                x,
                y,
                color="r",
                linewidth=3,
                linestyle="--",
                label=sv_labels['true'],
            )
        histo(
            Emp_Sing_Val,
            color="k",
            linewidth=3,
            ax=ax,
            label=sv_labels['empirical'],
        )
        plt.tick_params(axis="both", which="major", labelsize=15)
        plt.yticks([])
        if my_model != 0:
            plt.xlim(left=0)
        plt.legend(loc="upper right")
        if do_save:
            plt.savefig(f"{file_name}_{dimension_details}", bbox_inches="tight")
        plt.show()
    else:
        if my_model == 0:
            ax.plot(Emp_Sing_Val, Clean_Sing_Val, "b.")
            plt.xlabel(sv_labels['empirical'], fontsize=15)
            plt.ylabel(sv_labels['cleaned'], fontsize=15)
            plt.tick_params(axis="both", which="major", labelsize=15)
            plt.xlim(left=0)
            if do_save:
                plt.savefig(f"{file_name}_{dimension_details}", bbox_inches="tight")
            plt.show()
        else:
            x = np.linspace(min_s, max_s, Nlinspace)
            y = the_final_fancy_density(x)
            ax.plot(
                x,
                y,
                color="r",
                linewidth=3,
                linestyle="--",
                label=sv_labels['true'],
            )
            histo(
                Emp_Sing_Val,
                ax=ax,
                color="k",
                linewidth=3,
                label=sv_labels['empirical'],
            )
            histo(
                Clean_Sing_Val,
                ax=ax,
                color="b",
                linewidth=3,
                label=sv_labels['cleaned'],
            )
            plt.tick_params(axis="both", which="major", labelsize=15)
            plt.yticks([])
            plt.legend(loc="upper right")
            plt.xlim(left=0)
            if do_save:
                plt.savefig(f"{file_name}_{dimension_details}", bbox_inches="tight")
            plt.show()
            fig, ax = plt.subplots(figsize=figsize, tight_layout=True)
            ax.plot(True_s, Emp_Sing_Val, "k.", label=sv_labels['empirical'])
            ax.plot(True_s, Clean_Sing_Val, "b.", label=sv_labels['cleaned'])
            ax.plot(True_s, True_s, "r.", label=sv_labels['true'])
            plt.tick_params(axis="both", which="major", labelsize=15)
            plt.xlabel(sv_labels['true'], fontsize=15)
            plt.legend(loc="best")
            plt.ylim(bottom=0)
            if do_save:
                plt.savefig(file_name + f"_true_vs_emp_and_cleaned_{dimension_details}", bbox_inches="tight")
            plt.show()
            fig, ax = plt.subplots(figsize=figsize, tight_layout=True)
            ax.plot(Emp_Sing_Val, Emp_Sing_Val, "k.", label=sv_labels['empirical'])
            ax.plot(Emp_Sing_Val, Clean_Sing_Val, "b.", label=sv_labels['cleaned'])
            ax.plot(Emp_Sing_Val, True_s, "r.", label=sv_labels['true'])
            plt.tick_params(axis="both", which="major", labelsize=15)
            plt.xlabel(sv_labels['empirical'], fontsize=15)
            plt.legend(loc="best")
            plt.ylim(bottom=0)
            if do_save:
                plt.savefig(file_name + f"_emp_vs_true_and_cleaned_{dimension_details}", bbox_inches="tight")
            plt.show()


for my_model in [0, 1]:
    model_name="null_case" if my_model == 0 else "bimodal_density"
    for q in [0.1, 0.5]:
        if q == 0.1:
            alpha, beta = 0.1, 0.1
        else:
            alpha, beta = 0.5, 0.5
        T = 250 * factor_test if q == 0.1 else 10 * factor_test
        n, p = my_int(alpha * T), my_int(beta * T)
        True_s, Etotale = Total_Cov(my_model, n, p, T)
        (s, new_s, new_s_isotonic) = RIE_Cross_Covariance(CZZemp=Etotale,
                                                          T=T,
                                                          n=n,
                                                          p=p,
                                                          Return_Sing_Values_only=True)

        outdir = "data_and_figures/"
        outdir += sys.argv[0].split("/")[-1].replace(".py", "")
        outdir=os.path.join(outdir, model_name)
        dimension_details="n=" + str(n) + "_p=" + str(p) + "_T=" + str(T)
        outdir=os.path.join(outdir, dimension_details)
        os.makedirs(outdir, exist_ok=True)
        np.savetxt(outdir + "/true_sing_val.txt", s)
        np.savetxt(outdir + "/cleaned_sing_val.txt", new_s)
        np.savetxt(outdir + "/isotonic_cleaned_sing_val.txt", new_s_isotonic)
        for isotonic_flag in [0, 1]:
            the_new_s = new_s_isotonic if isotonic_flag else new_s
            if isotonic_flag == 0:
                plot_results(
                    my_model=my_model, True_s=True_s, Emp_Sing_Val=s, Clean_Sing_Val=the_new_s,
                    RIE_flag=0,
                    dimension_details=dimension_details,
                    file_name=os.path.join(outdir, f"{model_name}_true_vs_emp_sing_val")
                )

            plot_results(
                my_model=my_model, True_s=True_s, Emp_Sing_Val=s, Clean_Sing_Val=the_new_s,
                RIE_flag=1,
                dimension_details=dimension_details,
                file_name=os.path.join(outdir, f"{model_name}_true_vs_emp_sing_val_vs_RIE_isotonic={isotonic_flag}")
            )
