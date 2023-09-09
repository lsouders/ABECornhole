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

week_number = 0 # will store what week it currently is
# Attempt to cycle through and print each player
for index in df.index:
    #print("Player: ", df.loc[index, "Players"])
    # Get the stats for each player
    stats = []
    weeks_attended = int(df.loc[index, "Weeks Attended"])
    if weeks_attended > week_number:
        week_number  = weeks_attended
    for i in range(weeks_attended):
        stats.append(int(df.iloc[index, i+4])) # have to offset by 4 to account for avg's and week count infront of the weekly scores.
    # calculate weekly average, then average of best 5.
    stats.sort(reverse=True)
    sum = weekly_avg = best_avg = 0
    for i in range(weeks_attended):
        sum += stats[i]
        if i <= 4:
            best_avg = sum
    weekly_avg = sum // weeks_attended
    if weeks_attended > 5:
        best_avg //= 5
    else:
        best_avg //= weeks_attended 
    # print("Weekly:", weekly_avg, ", best 5:", best_avg)
    # Add the data to the proper column
    df.loc[index, "Weekly Average"] = weekly_avg
    df.loc[index, "Best 5 Weeks Avg"] = best_avg

# not sorting for some reason?
sorted_df = df.sort_values(by=["Best 5 Weeks Avg"], ascending=False)
print(sorted_df)
output_str = "Week" +str(week_number) + "Results.xlsx"
sorted_df.to_excel(output_str)