import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import math
import random

global count
global injected_credit
count = 0
injected_credit = False

def initialize_graph():
    G = nx.Graph()
    # Set positions for the bank nodes in a horizontal line with increased spacing
    bank_spacing = 10
    bank_positions = {f'Bank0{i+3}': (i * bank_spacing, 0) for i in range(5)}

    # Add the bank nodes with fixed positions and labels
    for bank, pos in bank_positions.items():
        G.add_node(bank, size=2000, pos=pos, label=bank, process='BANK', black=0, red=0, colour = 0)  # Initialize black and red sums to 0

    # Calculate and add the borrower nodes with the specified attributes
    num_borrowers_per_bank = 10
    borrower_node_radius = 3  # Distance from the bank node

    for bank, bank_pos in bank_positions.items():
        p_value = int(bank[-1])  # p attribute as per the connected bank
        bank_black = 0
        bank_red = 0
        for j in range(num_borrowers_per_bank):
            angle = 2 * math.pi * j / num_borrowers_per_bank
            borrower_pos = (bank_pos[0] + borrower_node_radius * math.cos(angle),
                            bank_pos[1] + borrower_node_radius * math.sin(angle))
            borrower_node_id = f'Borrower{bank[-2:]}{j}'
            black_attribute = random.randint(18, 20) # change randomness
            red_attribute = random.randint(16, 18) # change randomness
            colour_attribute = black_attribute / (red_attribute + black_attribute)
            G.add_node(borrower_node_id, size=100, pos=borrower_pos, label='', process='bobobo',
                       black=black_attribute, red=red_attribute, p=p_value, colour=colour_attribute)
            G.add_edge(bank, borrower_node_id, width=1)
            # Accumulate sums of black and red for the bank
            bank_black += black_attribute
            bank_red += red_attribute
        # Set the bank's black and red attributes
        G.nodes[bank]['black'] = bank_black
        G.nodes[bank]['red'] = bank_red
        # Calculate the bank's colour attribute
        G.nodes[bank]['colour'] = bank_black / (bank_black + bank_red)

    # Add edges between bank nodes with a width attribute for bold edges
    for i in range(4):
        G.add_edge(f'Bank0{i+3}', f'Bank0{i+4}', width=5)  # Use 'width' attribute to specify bold edges
    
    # Set the layout for the nodes
    pos = nx.get_node_attributes(G, 'pos')

    return G, pos

# Update function for the animation
def update_graph(num, G, pos, ax, cmap):
    global count, injected_credit
    # Open a file to write attributes
    with open('network_attributes.txt', 'a') as file:
        file.write(f"Time step {count}\n")
        count += 1
        # Perform the Pólya process for each borrower node
        for node in G.nodes(data=True):
            if 'p' in node[1]:  # Check if it's a borrower node
                p = node[1]['p']
                black = node[1]['black']
                red = node[1]['red']
                if random.random() < p/10:  # Polya process
                    if random.random() < black / (red + black):
                        node[1]['black'] += 1 # delta bi polya
                    else:
                        node[1]['red'] += 1 # delta ri polya
                else:  # Simple process
                    node[1]['red'] += 1 # delta bi stochastic
                # Update colour attribute
                node[1]['colour'] = node[1]['black'] / (node[1]['black'] + node[1]['red'])

            # Write the attributes to file
            file.write(f"{node[0]}: Black = {node[1]['black']}, Red = {node[1]['red']}\n")
        '''
CREDIT INJECTION A
        '''    
        # if (G.degree(f'Bank03') == 1 or G.degree(f'Bank04') == 2) and not injected_credit:
        #     # STRATEGY 1
        #     # G.nodes[f'Bank03']['black'] += 200 # credit amount
        #     # STRATEGY 2
        #     # G.nodes[f'Bank03']['black'] += 150 # credit amount
        #     # G.nodes[f'Bank04']['black'] += 50 # credit amount
        #     # STRATEGY 3
        #     # G.nodes[f'Bank03']['black'] += 100 # credit amount
        #     # G.nodes[f'Bank04']['black'] += 100 # credit amount
        #     injected_credit = True
        #     print(f"here is the time step: {count}")
        #     print(f"Hear is where the injected credit should be true: {injected_credit}")
        '''
CREDIT INJECTION B
        '''    
        # if (G.degree(f'Bank03') == 1 or G.degree(f'Bank04') == 2 or G.degree(f'Bank05') == 2) and not injected_credit:
        #     budget = 200
        #     a = G.nodes[f'Bank03']['red'] / G.nodes[f'Bank03']['black']
        #     b = G.nodes[f'Bank04']['red'] / G.nodes[f'Bank04']['black']
        #     c = G.nodes[f'Bank05']['red'] / G.nodes[f'Bank05']['black']
        #     total = a + b + c
        #     ratiosA = a / total
        #     ratiosB = b / total
        #     ratiosC = c / total

        #     G.nodes[f'Bank03']['black'] += int(ratiosA * budget)
        #     G.nodes[f'Bank04']['black'] += int(ratiosB * budget)
        #     G.nodes[f'Bank05']['black'] += int(ratiosC * budget)

        #     print(f"here is the ratio for bank03: {ratiosA}")
        #     print(f"here is the ratio for bank04: {ratiosB}")
        #     print(f"here is the ratio for bank05: {ratiosC}")
        #     injected_credit = True
        '''
CREDIT INJECTION C
        '''    
        if (G.degree(f'Bank03') == 1 or G.degree(f'Bank04') == 2 or G.degree(f'Bank05') == 2) and not injected_credit:
            # equal distribution
            G.nodes[f'Bank03']['black'] += 40 # credit amount
            G.nodes[f'Bank04']['black'] += 40 # credit amount
            G.nodes[f'Bank05']['black'] += 40 # credit amount
            G.nodes[f'Bank06']['black'] += 40 # credit amount
            G.nodes[f'Bank07']['black'] += 40 # credit amount
            injected_credit = True
            print(f"here is the time step: {count}")
            print(f"Hear is where the injected credit should be true: {injected_credit}")
   
        # Update bank nodes
        for i in range(3, 8):
            superurn_black = sum(G.nodes[n]['black'] for n in G.neighbors(f'Bank0{i}') if 'Bank' in n)
            superurn_black += G.nodes[f'Bank0{i}']['black']
            superurn_red = sum(G.nodes[n]['red'] for n in G.neighbors(f'Bank0{i}') if 'Bank' in n)
            superurn_red += G.nodes[f'Bank0{i}']['red']

            G.nodes[f'Bank0{i}']['black'] += 0 # arbitrary number bank income every time step

            if random.random() < (superurn_black / (superurn_black + superurn_red)):
                G.nodes[f'Bank0{i}']['black'] += 6 # arbitrary number
            else:
                G.nodes[f'Bank0{i}']['red'] += 5 # arbitrary number

            print(f'Bank0{i} Black: {superurn_black}')
            print(f'Bank0{i} Red: {superurn_red}')


            # for n in G.neighbors(f'Bank0{i}'): 
            #     if 'Borrower' in n:
            #         if G.nodes[n]['red'] > (2 * G.nodes[n]['black']): # default threshold if statement arbitrary threshold
            #             G.nodes[f'Bank0{i}']['red'] += (G.nodes[n]['red'] - G.nodes[n]['black'])
            #             G.remove_node(n)

            # Create a list to hold nodes to remove after iteration
            nodes_to_remove = []
            for n in G.neighbors(f'Bank0{i}'): 
                if 'Borrower' in n:
                    if G.nodes[n]['red'] >= (2 * G.nodes[n]['black']): # default threshold if statement arbitrary threshold
                        G.nodes[f'Bank0{i}']['red'] += (G.nodes[n]['red'] - G.nodes[n]['black'])
                        nodes_to_remove.append(n)  # Add this node to the list of nodes to remove

            # Remove the nodes after finishing the iteration
            for n in nodes_to_remove:
                G.remove_node(n)

            # bank_black = sum(G.nodes[n]['black'] for n in G.neighbors(f'Bank0{i}') if 'Borrower' in n)
            # bank_red = sum(G.nodes[n]['red'] for n in G.neighbors(f'Bank0{i}') if 'Borrower' in n)
            # G.nodes[f'Bank0{i}']['black'] = bank_black
            # G.nodes[f'Bank0{i}']['red'] = bank_red
            G.nodes[f'Bank0{i}']['colour'] = G.nodes[f'Bank0{i}']['black'] / (G.nodes[f'Bank0{i}']['black'] + G.nodes[f'Bank0{i}']['red'])

            # Write the bank attributes to file
            # file.write(f"Bank0{i}: Black = {bank_black}, Red = {bank_red}\n")
        print('\n')
        file.write("\n")  # Add a newline for separation between time steps

    # Clear previous nodes and edges
    ax.clear()
    plt.axis('off')

    # Recreate the drawing for the current frame
    node_colors = [cmap(G.nodes[n]['colour']) for n in G.nodes()]
    edge_widths = [5 if 'Bank' in u and 'Bank' in v else 1 for u, v in G.edges()]
    
    nx.draw_networkx_nodes(G, pos, node_size=[G.nodes[n]['size'] for n in G.nodes()], node_color=node_colors, ax=ax)
    nx.draw_networkx_edges(G, pos, width=edge_widths, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=8, ax=ax)


# Custom colormap
colors = [(1, 0, 0), (0, 0, 1)]  # Dark red to dark blue
cmap_name = 'dark_red_to_dark_blue'
custom_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=256)

# Use the function to initialize the graph
G, pos = initialize_graph()

# Create a figure for the animation
fig, ax = plt.subplots(figsize=(20, 10))
plt.axis('off')

# Set up the animation
ani = FuncAnimation(fig, update_graph, fargs=(G, pos, ax, custom_cmap), frames=10, interval=10000)

plt.show()