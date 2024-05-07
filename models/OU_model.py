import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates

# Modelo Ornstein Uhlenbeck
def simulate_ou_process4(mu, theta, sigma, X0, n_simulations, dt=1):
    X = []
    for i in range(n_simulations):
        noise = np.random.normal()
        p = X0 * np.exp(-theta*dt) + mu * (1 - np.exp(-theta*dt)) + sigma * np.sqrt((1 - np.exp(-2*theta*dt)) / (2*theta)) * noise
        X.append(p)
    return X

