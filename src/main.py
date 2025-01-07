import pandas as pd
import matplotlib.pyplot as plt
from Data import Data as D
from Results import Results as R

# Define Constants
CURR_SEASON = 'Winter25'
CURR_SEASON_MAIN_FILE = f'Winter25\\{CURR_SEASON}Main.csv'
INPUT_FILE = 'input.csv'

print(f"Options for the program currently are: \n\tStats\n\tGraph\n\tReadWeek\n\tWriteResults\n\tquit\n")

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
        case 'ReadWeek':
            R.update_results(INPUT_FILE)
        case 'WriteResults':
            filename = input('File to write to main: ')
            R.write_results_to_main(f'{CURR_SEASON}\\{filename}')
        case 'quit':
            break