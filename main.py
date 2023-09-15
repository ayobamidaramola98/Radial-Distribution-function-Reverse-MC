import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Set font properties
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'Times New Roman'
rcParams['font.size'] = 20

# Parameters
r_min = 0.0
r_max = 12.0
r_step = 0.05
density = 0.07
num_iterations = 60
num_avg_iterations = 10

# Generate g(r) function
def generate_gr(r):
    G1 = np.exp(-(r - 2.3)**2 / (2 * 0.25**2))
    G2 = np.exp(-(r - 4.4)**2 / (2 * 0.5**2))
    G3 = np.exp(-(r - 6.5)**2 / (2 * 1.0**2))
    Sf = 0.1 * r if r < 10 else 1.0
    xi = np.random.normal(scale=0.05)
    return 2.5 * G1 + 0.4 * G2 + 0.2 * G3 + Sf + xi

# Generate g(r) and save to PDF.txt
with open('PDF.txt', 'w') as f:
    for iteration in range(num_iterations):
        r_values = np.arange(r_min, r_max + r_step, r_step)
        gr_values = [generate_gr(r) for r in r_values]
        f.write("Iteration: #" + str(iteration + 1) + "\n")
        np.savetxt(f, np.column_stack((r_values, gr_values)))

# Monitor and calculate running average of g(r)
averaged_gr = np.zeros(len(r_values))
num_averaged = 0

with open('PDF.txt', 'r') as f:
    with open('PDF_average.txt', 'w') as avg_file:
        for line in f:
            if line.startswith('Iteration'):
                num_averaged += 1
                data = []
                for _ in range(len(r_values)):
                    try:
                        data.append(next(f).strip().split())
                    except StopIteration:
                        break
                if data:
                    data = np.asarray(data, dtype=np.float64)
                    averaged_gr += data[:, 1]
                    avg_gr = averaged_gr / num_averaged
                    avg_file.write("Frames averaged: #" + str(num_averaged) + "\n")
                    np.savetxt(avg_file, np.column_stack((r_values, avg_gr)))

# Calculate coordination number
coord_num = []
with open('PDF_average.txt', 'r') as avg_file:
    for line in avg_file:
        if line.startswith('Frames averaged'):
            data = []
            for _ in range(len(r_values)):
                try:
                    data.append(next(avg_file).strip().split())
                except StopIteration:
                    break
            if data:
                data = np.asarray(data, dtype=np.float64)
                r_values = data[:, 0]
                gr_values = data[:, 1]
                r_min_idx = np.argmin(gr_values)
                r_min = r_values[r_min_idx]
                cn = 4 * np.pi * density * np.trapz(gr_values[:r_min_idx] * r_values[:r_min_idx]**2, r_values[:r_min_idx])
                coord_num.append(cn)

# Plotting
iterations_to_plot = [1, 5, 10, 60]
avg_iteration_labels = [1, 5, 10, "Average"]
coord_num_labels = ["Coordination Number"]

fig, axs = plt.subplots(2, 1, figsize=(8, 10))

# Plot g(r)
axs[0].set_xlabel('r (Å)')
axs[0].set_ylabel('g(r)')
axs[0].set_title('Pair Distribution Function (g(r))')
for iteration in iterations_to_plot:
    data = []
    with open('PDF.txt', 'r') as f:
        for _ in range((iteration-1)*(len(r_values)+1) + 1):
            next(f)
        for _ in range(len(r_values)):
            try:
                data.append(next(f).strip().split())
            except StopIteration:
                break
    if data:
        data = np.asarray(data, dtype=np.float64)
        r_values = data[:, 0]
        gr_values = data[:, 1]
        axs[0].plot(r_values, gr_values, label="Iteration " + str(iteration))
axs[0].legend()

# Plot average g(r)
axs[1].set_xlabel('r (Å)')
axs[1].set_ylabel('g(r)')
axs[1].set_title('Averaged Pair Distribution Function (g(r))')
with open('PDF_average.txt', 'r') as avg_file:
    for line in avg_file:
        if line.startswith('Frames averaged'):
            data = []
            for _ in range(len(r_values)):
                try:
                    data.append(next(avg_file).strip().split())
                except StopIteration:
                    break
            if data:
                data = np.asarray(data, dtype=np.float64)
                r_values = data[:, 0]
                avg_gr = data[:, 1]
                axs[1].plot(r_values, avg_gr, label="Average")
axs[1].legend(["Average"])
plt.tight_layout()
plt.show()

# Plot coordination number
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(coord_num)+1), coord_num)
plt.xlabel('Iteration')
plt.ylabel('Coordination Number')
plt.title('Coordination Number')
plt.tight_layout()
plt.show()

