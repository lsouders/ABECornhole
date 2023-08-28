###
# This script will take input in the form of an excel spread sheet containing people and their weekly stats as well as the number of weeks that 
# they have attended. We will store the data into a pandas DataFrame, and calculate the following:
#   1. Average of the players' best 5 weeks.
#   2. The players' weekly average.
# We will then sort all of the players based on their 5-weeks best average, and dump this information into an excel spreadsheet
# or some other format that will be easily readable. 
#
# Author: Lucas Souders
###

import pandas as pd

# Start by reading in the excel sheet
read = False
while read == False:
    fileName = input("Enter the name of the file: ")
    try: 
        df = pd.read_excel(fileName)
        read = True
    except FileNotFoundError:
        print("File not found, please enter the correct name of the file.")

# print out the DataFrame (for testing purposes only)
# print(df)

# Get the players
# print(df[["Players"]])

# Attempt to cycle through and print each player
for index in df.index:
    print("Player: ", df.loc[index, "Players"])
    # Get the stats for each player
    for i in range(df.loc[index, "Weeks Attended"]):
        print("week", i+1, ":", df.iloc[index, i+2]) 