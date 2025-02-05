import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.backends.backend_pdf import PdfPages

def val_to_alpha(a, b, val, alpha_min=0.2, alpha_max=1):
    return (val - a) / (b - a) * (alpha_max - alpha_min) + alpha_min

def SIR(y, _, beta, gamma):
    S, I, _ = y
    dSdt = -beta*S*I
    dIdt = beta*S*I - gamma*I
    dRdt = gamma*I
    return [dSdt, dIdt, dRdt]

y0 = [0.99, 0.01, 0.0]
t = np.linspace(0, 200, 200)

for gamma in np.linspace(0.1, 0.5, 5):
    plt.figure(figsize=(6, 8))
    for beta in np.linspace(0.1, 0.5, 5):
        sol = odeint(SIR, y0, t, args=(beta, gamma))

        alpha = val_to_alpha(0.1, 0.5, beta)
        plt.subplot(311)
        plt.plot(t, sol[:, 0], color='C0', alpha=alpha, label=rf'$\beta$ = {beta:.2}')
        plt.subplot(312)
        plt.plot(t, sol[:, 1], color='C1', alpha=alpha, label=rf'$\beta$ = {beta:.2}')
        plt.subplot(313)
        plt.plot(t, sol[:, 2], color='C2', alpha=alpha, label=rf'$\beta$ = {beta:.2}')

    plt.subplot(311)
    plt.xlabel('Time')
    plt.ylabel('S(t)')
    plt.xlim(0, 200)
    plt.ylim(0, 1)
    plt.grid(linestyle='--', alpha=0.7)
    plt.legend(loc='upper right')
    plt.title(rf'$\gamma$ = {gamma:.2}')

    plt.subplot(312)
    plt.xlabel('Time')
    plt.ylabel('I(t)')
    plt.xlim(0, 200)
    plt.legend(loc='upper right')
    plt.grid(linestyle='--', alpha=0.7)

    plt.subplot(313)
    plt.xlabel('Time')
    plt.ylabel('R(t)')
    plt.xlim(0, 200)
    plt.ylim(0, 1)
    plt.legend(loc='lower right')
    plt.grid(linestyle='--', alpha=0.7)


    plt.tight_layout()


with PdfPages('p07.pdf') as pdf:
    for i in plt.get_fignums():
        pdf.savefig(plt.figure(i))
    plt.close()
