import pandas as pd
import matplotlib.pyplot as plt
from Data import Data as D
from Results import Results as R

# Define Constants
CURR_SEASON = 'Fall25'
CURR_SEASON_MAIN_FILE = f'{CURR_SEASON}\\{CURR_SEASON}Main.csv'
INPUT_FILE = 'input.csv'

def get_curr_season():
    return CURR_SEASON

print(f"Options for the program currently are: \n\tStats\n\tGraph\n\tReadWeek\n\tWriteResults\n\tquit\n\tAddMainData\n\tBuildSeasonMaster\n")

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
        case 'AddMainData':
            filename = input('Filename of data to add: ')
            season = input('Season: ')
            week = input('Week: ')
            D.read_data(filename, season, week, season_sort=4)
        case 'BuildSeasonMaster':
            append_file = input('File to append to season\'s master file: ')
            D.build_season_master(CURR_SEASON, append_file)
        case 'quit':
            break