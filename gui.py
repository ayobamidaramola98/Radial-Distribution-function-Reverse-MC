#### This code is original owned by Daramola Ayobami ############
##### contact: ayobamidaramola98@gmail.com for clarity#############
##### Prequisite: install python ############################

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Function to calculate g(r) based on the provided expression
def calculate_gr(r):
    # Parameters for the function components
    mu_sigma_values = [(2.3, 0.25), (4.4, 0.5), (6.5, 1.0)]
    amplitudes = [2.5, 0.4, 0.2]
    noise_amplitude = 0.05

    # Calculate the function components
    components = []
    for i, (mu, sigma) in enumerate(mu_sigma_values):
        gn = amplitudes[i] * np.exp(-((r - mu) / sigma)**2 / 2)
        components.append(gn)

    sf = np.where(r < 10, 0.1 * r, 1)
    xi = np.random.normal(0, noise_amplitude, len(r))

    # Calculate the overall g(r) function
    gr = np.sum(components, axis=0) + sf + xi

    return gr

# Function to calculate the coordination number
def calculate_coordination_number(r, gr, density):
    r_min_index = np.argmin(gr)
    r_min = r[r_min_index]
    cn = 4 * np.pi * density * np.trapz(gr * r**2, r)

    return cn, r_min

# Function to update the plots
# Function to update the plots
def update_plots():
    # Clear the previous plots
    axes1.cla()
    axes2.cla()

    # Plot g(r)
    axes1.plot(r_values, gr, label='g(r)')
    axes1.plot(r_values, avg_gr, label='Average g(r)')

    # Set plot labels
    axes1.set_xlabel('r (Å)')
    axes1.set_ylabel('g(r)')
    axes1.legend()

    # Plot coordination number
    iterations = range(len(cn_values))
    axes2.plot(iterations, cn_values)
    axes2.set_xlabel('Iteration')
    axes2.set_ylabel('Coordination Number')

    # Update the figure canvas
    canvas.draw()


# Function to start the generation of g(r)
def start_generation():
    global is_generating

    # Disable the start button and enable the pause and reset buttons
    start_button['state'] = tk.DISABLED
    pause_button['state'] = tk.NORMAL
    reset_button['state'] = tk.NORMAL

    # Start generating g(r)
    is_generating = True
    generate_gr()

# Function to pause/resume the generation of g(r)
def pause_generation():
    global is_generating

    if is_generating:
        # Disable the pause button and enable the start button
        pause_button['state'] = tk.DISABLED
        start_button['state'] = tk.NORMAL

        # Pause the generation
        is_generating = False
    else:
        # Disable the start button and enable the pause button
        start_button['state'] = tk.DISABLED
        pause_button['state'] = tk.NORMAL

        # Resume the generation
        is_generating = True
        generate_gr()

# Function to reset the plots and generation
def reset_plots():
    global is_generating, iteration, avg_gr, cn_values

    # Disable the pause and reset buttons, enable the start button
    pause_button['state'] = tk.DISABLED
    reset_button['state'] = tk.DISABLED
    start_button['state'] = tk.NORMAL

    # Reset variables
    is_generating = False
    iteration = 0
    avg_gr = np.zeros(len(r_values))
    cn_values = []

    # Clear the plots
    axes1.cla()
    axes2.cla()
    axes1.set_xlabel('r (Å)')
    axes1.set_ylabel('g(r)')
    axes2.set_xlabel('Iteration')
    axes2.set_ylabel('Coordination Number')
    canvas.draw()

# Function to generate g(r)
def generate_gr():
    global iteration, gr, avg_gr, cn_values

    # Generate g(r)
    gr = calculate_gr(r_values)

    # Calculate running average
    avg_gr = (avg_gr * iteration + gr) / (iteration + 1)

    # Calculate coordination number
    cn, _ = calculate_coordination_number(r_values, gr, density)
    cn_values.append(cn)

    # Update the plots
    update_plots()

    # Increment the iteration count
    iteration += 1

    # Check if generating should continue
    if is_generating:
        root.after(1000, generate_gr)  # Wait for 1 second before generating the next g(r)

# Create the GUI window
root = tk.Tk()
root.title('GR Generator GUI')

# Create a figure and axes for plotting
fig, (axes1, axes2) = plt.subplots(nrows=2, figsize=(8, 8))

# Create a canvas to display the plots
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create buttons
start_button = tk.Button(root, text='Start', command=start_generation)
start_button.pack(side=tk.LEFT, padx=10)

pause_button = tk.Button(root, text='Pause/Resume', command=pause_generation, state=tk.DISABLED)
pause_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(root, text='Reset', command=reset_plots, state=tk.DISABLED)
reset_button.pack(side=tk.LEFT, padx=10)

# Configuration
r_spacing = 0.05
r_range = (0, 12)
density = 0.04

# Generate the values for r
r_values = np.arange(r_range[0], r_range[1] + r_spacing, r_spacing)

# Initialize variables
is_generating = False
iteration = 0
gr = np.zeros(len(r_values))
avg_gr = np.zeros(len(r_values))
cn_values = []

# Run the GUI event loop
root.mainloop()

