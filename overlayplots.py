import re
import matplotlib.pyplot as plt

# Define the pattern to match each line containing Black and Red values and the ratio at the bottom of each block
pattern_bank = re.compile(r"Black=(\d+), Red=(\d+)")
pattern_ratio = re.compile(r"Ratio: (\d+\.\d+)")

def process_and_plot(file_path, plot_label):
    # Initialize lists to store computed and given ratios
    computed_ratios = []
    given_ratios = []

    # Load and read the data file
    with open(file_path, "r") as file:
        data = file.read()

    # Split the data into blocks for each time step
    time_steps = data.strip().split("Time step")

    # Extract and compute both given and computed ratios for each time step
    for step in time_steps[1:]:  # Skip the first split as it's just a prefix text
        banks = pattern_bank.findall(step)
        banks = [(int(black), int(red)) for black, red in banks]
        
        # Compute the sum of black and red attributes
        sum_black = sum(black for black, red in banks)
        sum_red = sum(red for black, red in banks)
        
        # Compute the ratio of sums and add to the list
        if sum_black != 0:
            computed_ratio = sum_red / sum_black
        else:
            computed_ratio = 0
        computed_ratios.append(computed_ratio)
        
        # Extract the given ratio directly from the text
        ratio_match = pattern_ratio.search(step)
        if ratio_match:
            given_ratio = float(ratio_match.group(1))
        else:
            given_ratio = 0
        given_ratios.append(given_ratio)

    # Plotting computed ratios for the current file
    # plt.plot(computed_ratios, label=f'{plot_label} Computed Ratio', linestyle='-', linewidth=2, alpha=0.7)
    plt.plot(given_ratios, label=f'{plot_label} Alpha Ratio', linewidth=4, alpha=0.99)

# Prepare the plot
plt.figure(figsize=(14, 8))

# Call the function for each file
# process_and_plot("baseline_attributes.txt", "No Injection")
process_and_plot("uniform_attributes.txt", "Uniform All Banks")
process_and_plot("uniform_central_attributes.txt", "Uniform Central Banks")
# process_and_plot("redOVERblack_attributes.txt", "Heuristic Red/Blue")
# process_and_plot("blackOVERred_attributes.txt", "Heuristic Blue/Red")
# process_and_plot("heuristic_attributes.txt", "Heuristic Connections")


# To add another file, uncomment and modify the next line with the correct path and label
# process_and_plot("/path/to/your/second_data_file.txt", "File 2")

# Finalizing the plot
plt.xlabel('Time Step')
plt.ylabel('Ratio')
plt.title('Heuristic Injection Strategies Performance of Financial Stress Over Time (alpha adjusted)')
plt.legend(fontsize='large')  # You can adjust the size as needed, e.g., 'medium', 'large', 20, etc.
plt.grid(True)
plt.show()
