# Re-importing necessary libraries and redefining data structures due to reset
import re
from collections import defaultdict
import matplotlib.pyplot as plt

# Re-initializing data structures for banks and borrowers
banks_data = defaultdict(lambda: {'Black': [], 'Red': []})
borrowers_groups = {
    'Bank03': ['Borrower03' + str(i) for i in range(0, 10)],
    'Bank04': ['Borrower04' + str(i) for i in range(0, 10)],
    'Bank05': ['Borrower05' + str(i) for i in range(0, 10)],
    'Bank06': ['Borrower06' + str(i) for i in range(0, 10)],
    'Bank07': ['Borrower07' + str(i) for i in range(0, 10)],
}
borrowers_presence = {bank: defaultdict(lambda: True) for bank in borrowers_groups}
removal_times = defaultdict(list)

# Process the file again to extract bank data and identify removal times of borrowers
file_path = 'network_attributes.txt'
previous_line = ""
current_time_step = 0

with open(file_path, 'r') as file:
    for line in file:
        # Extract bank data
        bank_match = re.match(r'(Bank\d{2}): Black = (\d+), Red = (\d+)', line)
        if bank_match:
            bank_id, black, red = bank_match.groups()
            banks_data[bank_id]['Black'].append(int(black))
            banks_data[bank_id]['Red'].append(int(red))
        
        # Track time step and borrower presence
        if 'Time step' in line:
            current_time_step = int(re.search(r'Time step (\d+)', line).group(1))
        else:
            for bank_id, borrowers in borrowers_groups.items():
                for borrower in borrowers:
                    if borrower in line:
                        borrowers_presence[bank_id][borrower] = True
                    elif borrowers_presence[bank_id][borrower]:  # Previously present but now missing
                        removal_times[bank_id].append(current_time_step)
                        borrowers_presence[bank_id][borrower] = False

# Plotting with removal times indicated
plt.figure(figsize=[15, 10])
for idx, (bank_id, data) in enumerate(banks_data.items(), start=1):
    if bank_id in ['Bank03', 'Bank04', 'Bank05', 'Bank06', 'Bank07']:
        plt.subplot(2, 3, idx)
        plt.plot(data['Black'], label='Black', color='black')
        plt.plot(data['Red'], label='Red', color='red')

        # Add vertical bars for each removal time step
        for removal_time in set(removal_times[bank_id]):  # Use set to remove duplicates
            plt.axvline(x=removal_time, color='gray', linestyle='--', alpha=0.7)

        plt.title(f'{bank_id} Black vs Red Numbers')
        plt.xlabel('Time Step')
        plt.ylabel('Number')
        plt.legend()

plt.tight_layout()
plt.show()
