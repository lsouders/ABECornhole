# Read in results from a week during a season. Combine with main sheet for that season and 
# export the results.

import pandas as pd
import config
from Alias import Alias
from Players import Players
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

SEASON = config.CURR_SEASON
MAIN_SEASON_FILE = f'{SEASON}\\{SEASON}Main.csv'
INPUT_FILE = 'input.csv'
LOGO = 'images\\logo.png'

# SEASON = 'Winter25'
# MAIN_SEASON_FILE = f'Test\\main.csv'
# INPUT_FILE = 'input.csv'

class Results:

    @staticmethod
    def create_html(df: pd.DataFrame, out_filename: str):
        # Export DataFrame to HTML
        # reformat indexing to give current 'place' people are in
        df.reset_index(inplace=True, drop=True)
        df.index += 1 
        html_table = df.to_html()  # Export DataFrame without index

        # Background image file path
        background_image = LOGO

        # Combine HTML with CSS for styling
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DataFrame Overlay</title>
            <link rel="stylesheet" href="../style.css">
        </head>
        <body>
            <h1>Fall 2025</h1>
            {html_table}
        </body>
        </html>
        """
        # Save the combined content to an HTML file
        with open(f"{out_filename}.html", "w") as file:
            file.write(html_content)
        return

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
    def get_wins_averages(data: list, weeks_attended: int) -> tuple[int, int]:
        if weeks_attended == 0: return 0, 0 
        wins   = [int(str(item).split('-')[0].strip()) for item in data]
        points = [int(str(item).split('-')[1].strip()) if (len(str(item).split('-')) == 2) else 0 for item in data]
        points.sort(reverse=False)
        wins.sort(reverse=True)
        pts_avg = round(sum(points[:5]) / 5, 1 ) if weeks_attended >= 5 else round( sum(points) / weeks_attended, 1)
        wins_avg  = round(sum(wins[:5]) / 5, 1) if weeks_attended >= 5 else round(sum(wins) / weeks_attended, 1)
        return wins_avg, pts_avg
    

    @staticmethod
    def add_player_to_df(player: str, dataframe: pd.DataFrame):
        new_player = {'Player' : player}
        for col in dataframe.columns:
            if col != 'Player':
                new_player[col] = 0
        df = pd.concat([dataframe, pd.DataFrame([new_player])], ignore_index=True)
        return df

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
                    print(f'Alias not found for {player}.')
                    name = input('Enter new player\'s name: ')
                    new_ind = Players.get_player(name)
                    Alias.add_alias(player, new_ind)
                else:
                    name = Players.get_player_by_index(a_ind)
            else: name = player
            # Have name, now update main sheet with info from the week
            points = input_df.loc[input_df['Team Name'] == player, 'Points For'].iloc[0]
            # Ensure that the player exists in the main file. If not, notify the console
            if not (main['Player'] == name).any():
                print(f"Player '{name}' does not exist in the main file!")
                decision = input(f'Input player into main file? \n\t(\'N\' for no, enter their name otherwise):')
                if decision != 'N':
                    main = Results.add_player_to_df(decision, main)
            main.loc[main['Player'] == name, week] = points
            main.loc[main['Player'] == name, 'Weeks Attended'] += 1
        # Get results for the player
        for name in main['Player'].to_list():
            data = list( main.loc[main['Player'] == name, 'Week 1' : 'Week 10'].values[0] )
            weeks_attended = int( main.loc[main['Player'] == name, 'Weeks Attended'].values[0] )
            weekly_avg, best5_avg = Results.get_averages(data, weeks_attended)
            main.loc[main['Player'] == name, 'Weekly Avg'] = weekly_avg
            main.loc[main['Player'] == name, 'Best 5 Weeks Avg'] = best5_avg
        main.sort_values(by=['Best 5 Weeks Avg', 'Weekly Avg'], inplace=True, ascending=False)
        return main, week_num
    
    @staticmethod
    def get_new_results(main: pd.DataFrame, input_df: pd.DataFrame):
        week_num = main['Weeks Attended'].max() + 1
        week = f'Week {week_num}'
        for player in input_df['Team Name'].to_list():
            # Need the player's true name, use alias functionality. Search for player first, then alias if not found
            p_ind = Players.get_player(player)
            if p_ind == -1:
                a_ind  = Alias.get_alias_by_name(player)
                if a_ind == -1:
                    print(f'Alias not found for {player}.')
                    name = input('Enter new player\'s name: ')
                    new_ind = Players.get_player(name)
                    Alias.add_alias(player, new_ind)
                else:
                    name = Players.get_player_by_index(a_ind)
            else: name = player
            # Have name, now update main sheet with info from the week
            points = input_df.loc[input_df['Team Name'] == player, 'Points Against'].iloc[0]
            wins   = input_df.loc[input_df['Team Name'] == player, 'Wins'].iloc[0]
            data_point = f'{wins} - {points}'
            # Ensure that the player exists in the main file. If not, notify the console
            if not (main['Player'] == name).any():
                print(f"Player '{name}' does not exist in the main file!")
            main.loc[main['Player'] == name, week] = data_point
            main.loc[main['Player'] == name, 'Weeks Attended'] += 1
        # Get results for the player
        for name in main['Player'].to_list():
            data = list( main.loc[main['Player'] == name, 'Week 1' : 'Week 10'].values[0] )
            weeks_attended = int( main.loc[main['Player'] == name, 'Weeks Attended'].values[0] )
            wins_avg, best5_avg = Results.get_wins_averages(data, weeks_attended)
            main.loc[main['Player'] == name, 'Wins'] = wins_avg
            main.loc[main['Player'] == name, 'Points Against'] = best5_avg
        main.sort_values(by=['Wins', 'Points Against'], inplace=True, ascending=[False, True])
        return main, week_num

    # Take df input to write out to results file
    @staticmethod
    def write_results(df: pd.DataFrame, filename: str):
        df.to_csv(filename, index=False)
        return 
    

    # Write out the verified results to the main file
    @staticmethod
    def write_results_to_main(filename: str):
        results = pd.read_csv(filename)
        Results.write_results(results, MAIN_SEASON_FILE)
    

    # Main method for updating results for a week
    @staticmethod
    def update_results(inp_file: str):
        main, input = Results.read_files(inp_file)
        results, week_num = Results.get_new_results(main, input)
        Results.write_results(results, f'{SEASON}\\Week{week_num}Results.xlsx') # xlsx for upload to google drive. Will delete after season
        Results.write_results(results, f'{SEASON}\\Week{week_num}Results.csv')  # csv for data wrangling (application uses csv)
        Results.create_html(results, f'{SEASON}\\Week{week_num}Results')
        return

# Results.update_results(INPUT_FILE)

#=======================================
# CODE TO RESET MAIN FILE
# main = pd.read_csv(MAIN_SEASON_FILE)
# main.loc[:, 'Best 5 Weeks Avg' : 'Week 10'] = 0
# main.to_csv(MAIN_SEASON_FILE, index=False)
#=======================================


# Test code to test new ranking system (Wins Total 5 Weeks/Best 5 Avg)
# main = pd.read_csv('Test\\main.csv')

# # Read 10 Weeks of input files
# for i in range(1, 11):
#     input_df = pd.read_csv(f'Test\\input_{i}.csv')
#     results, _ = Results.get_new_results(main, input_df)

#     # Update main df
#     main = results

# main.reset_index(drop=True, inplace=True)
# main.index += 1
# Results.create_html(main, 'Test\\results')
# print(main.head())

# Test set for weekly data decomposition
# data = ['184 - 8', '184 - 7', '188 - 7', '0', '0', '174 - 7', '158 - 7', '185 - 7', '154 - 6', '147 - 6']
# points = [int(str(item).split('-')[0]) for item in data]
# wins   = [ int(str(item).split('-')[1]) if (len(str(item).split('-')) == 2) else 0 for item in data]
# print(f'wins: \n{wins}')
# print(f'points: \n{points}')

print(SEASON) 