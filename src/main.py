import pandas as pd
from Data import Data as D
import matplotlib.pyplot as plt

print(f"Options for the program currently are: \n\tStats\n\tGraph\n")

# main program loop
while True:
    print(f'\n<><><><><><><><><><><><><><><><><><><><><><>\n')
    option = input(f"Option: ")
    
    match option:
        case 'Graph':
            name = input(f'Player Name: ')
            if name == 'quit': break
            season = input(f'Season: ')
            stat = input(f'Stat: ')
            D.graph(name, stat, season)
        case 'Stats':
            name = input(f'Player Name: ')
            season = input(f'Season: ')
            D.get_stats(name, season)