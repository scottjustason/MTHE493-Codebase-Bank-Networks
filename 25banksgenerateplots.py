import re
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Define or initialize your dictionaries here
black_attributes = defaultdict(list)
red_attributes = defaultdict(list)

# Pattern to match the lines with bank data
pattern = re.compile(r"Bank (\d+): Black=(\d+), Red=(\d+)")

# Function to read the file and populate the dictionaries
def read_bank_attributes(filename):
    with open(filename, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                bank_id, black, red = match.groups()
                black_attributes[bank_id].append(int(black))
                red_attributes[bank_id].append(int(red))

# Function to plot the bank ratio data
def plot_bank_ratio(bank_range, title):
    plt.figure(figsize=(10, 6))
    all_ratios = []  # To store the ratio of each bank for averaging
    
    for bank_id in bank_range:
        bank_id_str = str(bank_id)
        if bank_id_str in black_attributes and bank_id_str in red_attributes:
            ratio = [red / black if black > 0 else 0 for red, black in zip(red_attributes[bank_id_str], black_attributes[bank_id_str])]
            plt.plot(ratio, label=f"Bank {bank_id_str} Ratio (Red/Blue)", alpha=0.5)  
            all_ratios.append(ratio)
    
    if all_ratios:
        average_ratio = np.mean(all_ratios, axis=0)
        plt.plot(average_ratio, label="Average Ratio (Red/Blue)", linewidth=2.5, color='black')
    
    plt.xlabel("Time Step")
    plt.ylabel("Ratio (Red/Black)")
    plt.title(title)
    plt.legend()
    plt.show()

# Make sure to call the function to read attributes before plotting
filename = 'uniform_attributes.txt'
read_bank_attributes(filename)

# Then plot the data for each bank range
central_banks_range = range(1, 5)
middle_banks_range = range(5, 19)
outer_banks_range = range(19, 26)
all_banks_range = range(1, 26)


plot_bank_ratio(central_banks_range, "Central Banks 1-4 Ratio Over Time")
plot_bank_ratio(middle_banks_range, "Middle Banks 5-18 Ratio Over Time")
plot_bank_ratio(outer_banks_range, "Outer Banks 19-25 Ratio Over Time")
plot_bank_ratio(all_banks_range, "All Banks 1-25 Ratio Over Time")
