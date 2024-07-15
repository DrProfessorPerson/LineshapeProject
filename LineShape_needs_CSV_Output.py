import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

def lorentzian(x, mu, gamma, amplitude):
    """Generate Lorentzian distribution values."""
    return amplitude * (gamma**2) / ((x - mu)**2 + gamma**2)

def create_lineshape(multiplicity, center, gamma, amplitude=1, num_points=5000):
    """
    Generate a Lorentzian lineshape for a given multiplicity.
    multiplicity: int from 1 to 9, representing singlet to nonet
    center: float, the center position of the lineshape
    gamma: float, half-width at half-maximum of the Lorentzian
    amplitude: float, peak amplitude of the Lorentzian
    num_points: int, number of points for the x array (resolution)
    """
    if multiplicity < 1 or multiplicity > 9:
        raise ValueError("Multiplicity must be an integer between 1 and 9")
    
    x = np.linspace(-1.5, 1.5, num_points)
    y = np.zeros_like(x)
    
    # For multiplets, create positions around the center
    spacing = 2 / (multiplicity - 1) if multiplicity > 1 else 0  # Adjust the spacing as necessary
    positions = np.linspace(center - (multiplicity - 1) * spacing / 2, center + (multiplicity - 1) * spacing / 2, multiplicity)
    intensities = np.array([comb(multiplicity - 1, i) for i in range(multiplicity)])
    intensities = intensities / sum(intensities)  # Normalize intensities to sum to 1
    
    # Generate the lineshape
    for pos, inten in zip(positions, intensities):
        y += lorentzian(x, pos, gamma, amplitude * inten)
    
    return x, y

def plot_lineshape(multiplicity, center=0, gamma=0.05, amplitude=1, num_points=5000):
    """Plot Lorentzian lineshape for a given multiplicity."""
    plt.figure(figsize=(12, 8))
    
    x, y = create_lineshape(multiplicity, center, gamma, amplitude, num_points)
    plt.plot(x, y, label=f'Multiplicity {multiplicity}')
    
    plt.title(f'Lorentzian Lineshape for Multiplicity {multiplicity}')
    plt.xlabel('Position')
    plt.ylabel('Intensity')
    # plt.legend()
    plt.grid(False)
    plt.xlim(-2, 2)  # Confine x-axis between -1 and 1
    plt.show()

# Get user input for multiplicity
while True:
    try:
        user_input = int(input("Enter the multiplicity (1 for singlet, up to 9 for nonet): "))
        if 1 <= user_input <= 9:
            break
        else:
            print("Please enter an integer between 1 and 9.")
    except ValueError:
        print("Invalid input. Please enter an integer between 1 and 9.")

# Get user input for gamma
while True:
    try:
        gamma = float(input("Enter the half-width at half-maximum (gamma) for the Lorentzian lineshape [0.05 recommended, larger = broader peak]: "))
        if gamma > 0:
            break
        else:
            print("Please enter a positive number for gamma.")
    except ValueError:
        print("Invalid input. Please enter a positive number for gamma.")

# Plot the requested lineshape with higher resolution
plot_lineshape(user_input, gamma=gamma)
