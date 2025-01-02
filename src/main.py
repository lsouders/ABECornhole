import pandas as pd
from Data import Data as D
import matplotlib.pyplot as plt

# Define Constants
CURR_SEASON = 'Winter25'
CURR_SEASON_MAIN_FILE = 'WinterLeague25\\ABE Cornhole - Winter League.csv'
INPUT_FILE = 'input.csv'

print(f"Options for the program currently are: \n\tStats\n\tGraph\n\tReadWeek\n\tquit\n")

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
            main = pd.read_csv(CURR_SEASON_MAIN_FILE)
            main.fillna(0, inplace=True)

            # Read results into the dataframe. Use functionality from stats.py to make computations.
            # Can bring in functions from stats into its own file in src. Don't modify stats in main 
            # directory as it currently does what we need it to. input.csv will be the name of the weekly
            # results that we downloaded from scoreholio. Read in the data then delete the file once results
            # are verified (or maintain until end of season? Can rename to week# once used.)

            # Write out results to a weekly file
            
        case 'quit':
            break