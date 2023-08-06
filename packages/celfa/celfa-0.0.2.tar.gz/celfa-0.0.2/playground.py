import matplotlib.pyplot as plt
import numpy as np
import random

# Define the energy range
E = np.linspace(0, 2, 100)

# Define the chemical potentials
mu1 = 0.7
mu2 = 1.2
mu3 = 1.7

# Round the chemical potentials to the first digit after the dot
mu1 = round(mu1, 1)
mu2 = round(mu2, 1)
mu3 = round(mu3, 1)

# Calculate the Fermi-Dirac distribution functions
f1 = 1-np.heaviside(E - mu1, 0)
f2 = 1-np.heaviside(E - mu2, 0)
f3 = 1-np.heaviside(E - mu3, 0)

# Plot the Fermi-Dirac distribution functions
plt.plot(E, f1, label=r'$\mu_1 = {}$ eV'.format(mu1))
plt.plot(E, f2, label=r'$\mu_2 = {}$ eV'.format(mu2))
plt.plot(E, f3, label=r'$\mu_3 = {}$ eV'.format(mu3))

# Add labels and legend
plt.xlabel(r'$E$ (eV)')
plt.ylabel(r'$f(E)$')
plt.legend()

# Show the plot
plt.show()