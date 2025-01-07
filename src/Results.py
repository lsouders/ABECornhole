# Read in results from a week during a season. Combine with main sheet for that season and 
# export the results.

import pandas as pd
from Alias import Alias
from Players import Players
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

SEASON = 'Winter25'
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
        html_table = df.to_html(index=False)  # Export DataFrame without index

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
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1>Winter 2025</h1>
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
    

    # Take df input to write out to results file
    @staticmethod
    def write_results(df: pd.DataFrame, filename: str):
        # reformat indexing to give current 'place' people are in
        df.reset_index(inplace=True, drop=True)
        df.index += 1 
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
        results, week_num = Results.get_results(main, input)
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