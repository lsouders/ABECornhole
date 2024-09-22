import pandas as pd
import json

# Get the main datasheet. Drop rows where there is no name
main_df = pd.read_excel("Test.xlsx")
main_df = main_df.dropna( subset=['Players'] )

# Read in the results from the current weeks game.
results = pd.read_csv("RoundRobin.csv")
input_df = results[['Team Name', 'Points For', 'Points Against']]
input_df = input_df.rename( columns={'Team Name': 'Players'} )
# Get the players from this weeks game
players = input_df['Players'].to_list()

# Read in the names from the json
with open('names.json', 'r') as names_file:
    names = json.load( names_file )

# update names in 'names' dictionary


# Attempt to combine results into main file. If a player is not found, prompt user.
for row_num in range( len( input_df ) ):
    player = results.iloc[ row_num ][ 1 ]
    break