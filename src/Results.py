# Read in results from a week during a season. Combine with main sheet for that season and 
# export the results.

import pandas as pd
from Alias import Alias
from Players import Players

SEASON = 'Winter25'
MAIN_SEASON_FILE = f'{SEASON}\\{SEASON}Main.csv'
INPUT_FILE = 'input.csv'
# SEASON = 'Winter25'
# MAIN_SEASON_FILE = f'Test\\main.csv'
# INPUT_FILE = 'input.csv'

class Results:

    @staticmethod
    def read_files(inp_name: str):
        df = pd.read_csv(MAIN_SEASON_FILE)
        df.fillna(0, inplace=True)
        inp = pd.read_csv(inp_name)
        inp.fillna(0, inplace=True)
        return df, inp
    

    @staticmethod
    def get_averages(data: list, weeks_attended: int) -> tuple[int, int]:
        if weeks_attended == 0: return 0, 0 
        data.sort(reverse=True)
        weekly_avg = round( sum(data) / weeks_attended, 1)
        best5_avg = round( sum(data[:5]) / 5, 1 ) if weeks_attended >= 5 else round( sum(data) / weeks_attended, 1)
        return weekly_avg, best5_avg


    @staticmethod
    def get_results(main: pd.DataFrame, input_df: pd.DataFrame):
        week_num = main['Weeks Attended'].max() + 1
        week = f'Week {week_num}'
        for player in input_df['Team Name'].to_list():
            # Need the player's true name, use alias functionality. Search for player first, then alias if not found
            p_ind = Players.get_player(player)
            if p_ind == -1:
                a_ind  = Alias.get_alias_by_name(player)
                if a_ind == -1:
                    print('No Alias')
                    name = input('Enter new player\'s name: ')
                    new_ind = Players.add_player(name)
                    Alias.add_alias(player, new_ind)
                else:
                    name = Players.get_player_by_index(a_ind)
            else: name = player
            # Have name, now update main sheet with info from the week
            points = input_df.loc[input_df['Team Name'] == player, 'Points For'].iloc[0]
            main.loc[main['Player'] == name, week] = points
            main.loc[main['Player'] == name, 'Weeks Attended'] += 1
        # Get results for the player
        for name in main['Player'].to_list():
            data = list( main.loc[main['Player'] == name, 'Week 1' : 'Week 10'].values[0] )
            weeks_attended = int( main.loc[main['Player'] == name, 'Weeks Attended'].values[0] )
            weekly_avg, best5_avg = Results.get_averages(data, weeks_attended)
            main.loc[main['Player'] == name, 'Weekly Avg'] = weekly_avg
            main.loc[main['Player'] == name, 'Best 5 Weeks Avg'] = best5_avg
        return main, week_num
    

    # Take df input to write out to results file
    @staticmethod
    def write_results(df: pd.DataFrame, filename: str):
        df.to_csv(filename, index=False)
        return 
    
    # Main method for updating results for a week
    @staticmethod
    def update_results(file):
        main, input = Results.read_files()
        results, week_num = Results.get_results(main, input)
        Results.write_results(results, f'{SEASON}\\Week{week_num}Results.xlsx') # xlsx for upload to google drive. Will delete after season
        Results.write_results(results, f'{SEASON}\\Week{week_num}Results.csv')  # csv for data wrangling (application uses csv)
        Results.write_results(results, MAIN_SEASON_FILE)
        return 1

# main, inp = Results.read_files(f'Test\\input{2}.csv')
# main = Results.get_results(main, inp)
# for i in range(3, 11):
#     _, inp = Results.read_files(f'Test\\input{i}.csv')
#     main = Results.get_results(main, inp)
# # main, _ = Results.read_files(f'Test\\input{i}.csv')
# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
# print(main.sort_values(by=['Best 5 Weeks Avg', 'Weekly Avg'], ascending=False))
# main.to_csv('main.xlsx', index=False)