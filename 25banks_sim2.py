# Same as other 25banks.py script but different condition for credit injection
# Here we inject credit once the 'ratio' value excedes threshold = 1.4

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import numpy as np
import random
from matplotlib.animation import FuncAnimation

global count
global injected_credit
global ratio
global alpha_ratio
global alpha_cental
global alpha_middle
global alpha_small
global threshold
alpha_ratio = 0
alpha_cental = 0.5
alpha_middle = 0.35
alpha_small = 0.15
threshold = 1.4
count = 0
injected_credit = False
ratio = 0.0

# Redefine the functions after reset
def initialize_graph_with_attributes():
    G = nx.Graph()
    central_banks = [1, 2, 3, 4]
    other_banks = list(range(5, 26))
    all_banks = central_banks + other_banks

    G.add_nodes_from(all_banks)
    for i in central_banks:
        for j in central_banks:
            if i != j:
                G.add_edge(i, j)
        for node in other_banks:
            G.add_edge(i, node)
    for i in range(14):
        for j in range(i + 1, 14):
            G.add_edge(other_banks[i], other_banks[j])
    sequential_other_banks = other_banks[14:]
    for i in range(len(sequential_other_banks) - 1):
        G.add_edge(sequential_other_banks[i], sequential_other_banks[i + 1])

    pos = {1: [1, 1], 2: [1, -1], 3: [-1, -1], 4: [-1, 1]}
    pos.update({other_banks[i]: [np.cos(2 * np.pi * i / 21) * 3, np.sin(2 * np.pi * i / 21) * 3] for i in range(21)})
    node_sizes = {bank: 800 for bank in central_banks}
    node_sizes.update({bank: 400 for bank in other_banks})

    # Add 10 new Borrowers for each Bank, connect them, and define their positions, sizes, and attributes
    last_node = max(all_banks)
    for bank in all_banks:
        p_range = (0.6, 0.7) if bank in central_banks else ((0.45, 0.55) if bank <= 12 else (0.3, 0.4))
        bank_black = 0
        bank_red = 0
        for i in range(10):
            new_node = last_node + 1
            G.add_node(new_node)
            G.add_edge(bank, new_node)
            angle = 2 * np.pi * i / 10  # Spread Borrowers evenly around the Bank
            pos[new_node] = pos[bank] + np.array([np.cos(angle), np.sin(angle)]) * 0.5
            node_sizes[new_node] = 150  # Very small size for Borrowers
            # Borrower attributes
            black_value = random.randint(18, 20)
            red_value = random.randint(16, 18)
            G.nodes[new_node]['black'] = black_value
            G.nodes[new_node]['red'] = red_value
            G.nodes[new_node]['isBank'] = False
            p_value = random.uniform(*p_range)
            G.nodes[new_node]['p'] = p_value
            G.nodes[new_node]['s'] = 1 - p_value # useless right now
            # Sum of black and red values to initialize Bank attributes
            bank_black += black_value
            bank_red += red_value
            last_node = new_node
        # Set the Bank's attributes based on the total from its Borrowers
        G.nodes[bank]['black'] = bank_black
        G.nodes[bank]['red'] = bank_red
        G.nodes[bank]['isBank'] = True


    for bank in all_banks:
        G.nodes[bank]['superurn_black'] = G.nodes[bank]['black']  # Start with the bank's own attributes
        G.nodes[bank]['superurn_red'] = G.nodes[bank]['red']
        for connected_bank in G.neighbors(bank):
            if G.nodes[connected_bank]['isBank'] == True: # Making sure it's not a Borrower
                G.nodes[bank]['superurn_black'] += G.nodes[connected_bank]['black']
                G.nodes[bank]['superurn_red'] += G.nodes[connected_bank]['red']
        # print(G.nodes[bank]['superurn_black'])
        # print(G.nodes[bank]['superurn_red'])

    return G, pos, node_sizes


def update_graph_gradient(num, G, pos, node_sizes, ax):
    global count, injected_credit, ratio, alpha_middle, alpha_cental, alpha_small, alpha_ratio
    if count == 1000:  # Check if count has reached 1000
        plt.close()  # Close the figure, effectively stopping the animation
        return  # Exit the function to prevent further execution
    borrowers_to_remove = []
    for borrower in [n for n, d in G.nodes(data=True) if 'p' in d]:
        p_value = G.nodes[borrower]['p']
        random_number = random.random()
        if p_value > random_number:
            if random.random() < G.nodes[borrower]['black'] / (G.nodes[borrower]['black'] + G.nodes[borrower]['red']):
                G.nodes[borrower]['black'] += 1
            else:
                G.nodes[borrower]['red'] += 1
        else:
            G.nodes[borrower]['red'] += 1
        
        if G.nodes[borrower]['black'] > 0:  # Avoid division by zero
            ratio = G.nodes[borrower]['red'] / G.nodes[borrower]['black']
            if ratio > 2:
                connected_bank = next(G.neighbors(borrower))
                G.nodes[connected_bank]['red'] += G.nodes[borrower]['red'] - G.nodes[borrower]['black']
                borrowers_to_remove.append(borrower)

    for borrower in borrowers_to_remove:
        G.remove_node(borrower)
        del pos[borrower]
        del node_sizes[borrower]

    '''CREDIT INJECTION - Uniform Solution - Over all banks'''
    # budget = 0
    # if injected_credit == False:
    #     print(alpha_ratio)
    #     if alpha_ratio > threshold:
    #         for i in range(1, 26):
    #             budget += G.nodes[i]['black']
    #         budget = int(0.123*budget) # Budget is 12.3% of total black balls at time of first failure
    #         balls_per_bank = int(budget / 25) # For uniform solution
    #         print(f"Timestep: {count}")            
    #         print(f"Budget: {budget}")
    #         print(f"bpb: {balls_per_bank}") 
    #         for i in range(1, 26):
    #             G.nodes[i]['black'] += balls_per_bank
    #         injected_credit = True           
    '''CREDIT INJECTION - Uniform Solution - Over Central Banks'''
    budget = 0
    if injected_credit == False:
        print(alpha_ratio)
        if alpha_ratio > threshold:
            for i in range(1, 26):
                budget += G.nodes[i]['black']
            budget = int(0.123*budget) # Budget is 12.3% of total black balls at time of first failure
            balls_per_bank = int(budget / 4) # For uniform solution
            print(f"Timestep: {count}")            
            print(f"Budget: {budget}")
            print(f"bpb: {balls_per_bank}") 
            for i in range(1, 5):
                G.nodes[i]['black'] += balls_per_bank
            injected_credit = True  
    '''CREDIT INJECTION - Heuristic Solution - Inject entire budget into central bank 
    with highest red/black ratio'''
    # budget = 0
    # highest_ratio = []
    # if injected_credit == False:
    #     print(alpha_ratio)
    #     if alpha_ratio > threshold:
    #         for i in range(1, 26):
    #             budget += G.nodes[i]['black']
    #         budget = int(0.123*budget) # Budget is 12.3% of total black balls at time of first failure
    #         for bank in range(1, 5):
    #             highest_ratio.append(G.nodes[bank]['red']/G.nodes[bank]['black'])
    #         print(highest_ratio) # Testing
    #         print(max(highest_ratio)) # Testing
    #         high = max(highest_ratio)
    #         index = highest_ratio.index(high)
    #         print(index) # Testing
    #         print(G.nodes[index+1]['black']) # Testing
    #         G.nodes[index+1]['black'] += budget
    #         print(G.nodes[index+1]['black']) # Testing
    #         injected_credit = True 
    '''CREDIT INJECTION - Heuristic Solution - Inject entire budget into central bank 
    with highest black/red ratio'''
    # budget = 0
    # highest_ratio = []
    # if injected_credit == False:
    #     print(alpha_ratio)
    #     if alpha_ratio > threshold:
    #         for i in range(1, 26):
    #             budget += G.nodes[i]['black']
    #         budget = int(0.123*budget) # Budget is 12.3% of total black balls at time of first failure
    #         for bank in range(1, 5):
    #             highest_ratio.append(G.nodes[bank]['black']/G.nodes[bank]['red'])
    #         print(highest_ratio) # Testing
    #         print(max(highest_ratio)) # Testing
    #         high = max(highest_ratio)
    #         index = highest_ratio.index(high)
    #         print(index) # Testing
    #         print(G.nodes[index+1]['black']) # Testing
    #         G.nodes[index+1]['black'] += budget
    #         print(G.nodes[index+1]['black']) # Testing
    #         injected_credit = True   
    '''CREDIT INJECTION - Heuristic Solution - majority to central banks
       relative to number of edges to total edges in network'''
    # budget = 0
    # if injected_credit == False:
    #     if alpha_ratio > threshold:
    #         for i in range(1, 26):
    #             budget += G.nodes[i]['black']
    #         budget = int(0.123*budget) # Budget is 12.3% of total black balls at time of first failure
            
    #         print(f"Timestep: {count}")            
    #         print(f"Budget: {budget}")
    #         for i in range(1, 5):
    #             G.nodes[i]['black'] += int((24/376) * budget) # central banks have 24 connections
    #         for i in range(5, 19):
    #             G.nodes[i]['black'] += int((17/376) * budget) # middle banks have 17 connections
    #         for i in range(19, 26):
    #             G.nodes[i]['black'] += int((6/376) * budget) # small banks have 6 connections
    #         injected_credit = True     
   
    for bank in range(1, 26):
        if random.random() < (G.nodes[bank]['superurn_black'] / (G.nodes[bank]['superurn_black'] + G.nodes[bank]['superurn_red'])):
            G.nodes[bank]['black'] += 6 # arbitrary
        else:
            G.nodes[bank]['red'] += 5 # arbitrary

    for bank in range(1, 26):
        G.nodes[bank]['superurn_black'] = G.nodes[bank]['black']
        G.nodes[bank]['superurn_red'] = G.nodes[bank]['red']
        for connected_bank in G.neighbors(bank):
            if G.nodes[connected_bank]['isBank'] == True: # Making sure it's not a Borrower
                G.nodes[bank]['superurn_black'] += G.nodes[connected_bank]['black']
                G.nodes[bank]['superurn_red'] += G.nodes[connected_bank]['red']
        # print(G.nodes[bank]['superurn_black'])
        # print(G.nodes[bank]['superurn_red'])


    ax.clear()

    # Custom colormap
    
    colors = [(0, 0, 0.8), (1, 0, 0)]  # Dark red to dark blue
    
    cmap_name = 'dark_red_to_dark_blue'
    custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)

    nx.draw(G, pos, ax=ax, node_size=[node_sizes[node] for node in G.nodes()],
            node_color=[custom_cmap(G.nodes[n]['red'] / (G.nodes[n]['black'] + G.nodes[n]['red'])) for n in G.nodes()],
            cmap='coolwarm', vmin=0, vmax=1, with_labels=False, edge_color='gray')
    ax.set_title("Time step: " + str(count))
    count += 1
    # ax.clear()
    # nx.draw(G, pos, ax=ax, node_size=[node_sizes[node] for node in G.nodes()],
    #         node_color=[G.nodes[n]['red'] / (G.nodes[n]['black'] + G.nodes[n]['red']) for n in G.nodes()],
    #         cmap='coolwarm', vmin=0, vmax=1, with_labels=False, edge_color='gray')
    # ax.set_title("Time step: " + str(count))
    # count += 1

    # Write the 'black' and 'red' attributes of all Banks to a text file at each time step
    with open('bank_attributes.txt', 'a') as file:
        file.write(f"Time step {count}:\n")
        red_sum = 0
        black_sum = 0
        for bank in range(1, 26):  # Loop through all banks
            if bank <= 4:
                red_sum += (alpha_cental*G.nodes[bank]['red'])
                black_sum += (alpha_cental*G.nodes[bank]['black'])
            elif bank <= 18:
                red_sum += (alpha_middle*G.nodes[bank]['red'])
                black_sum += (alpha_middle*G.nodes[bank]['black'])
            else:
                red_sum += (alpha_small*G.nodes[bank]['red'])
                black_sum += (alpha_small*G.nodes[bank]['black'])
            black = G.nodes[bank]['black']
            red = G.nodes[bank]['red']
            # black_sum += G.nodes[bank]['black']
            # red_sum += G.nodes[bank]['red']
            file.write(f"Bank {bank}: Black={black}, Red={red}\n")
        ratio = red_sum/black_sum
        alpha_ratio = ratio
        file.write(f"Ratio: {ratio}")
        file.write("\n")  # Add a newline for separation between time steps
        file.write("\n")  # Add a newline for separation between time steps


# Reset the global counter and recreate the graph for the gradient animation
count = 0
G_gradient, pos_gradient, node_sizes_gradient = initialize_graph_with_attributes()
fig_gradient, ax_gradient = plt.subplots(figsize=(8, 8))
ani_gradient = FuncAnimation(fig_gradient, update_graph_gradient, frames=50, interval=10, fargs=(G_gradient, pos_gradient, node_sizes_gradient, ax_gradient))

plt.show()  



