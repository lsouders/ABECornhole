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
import os

# Start by reading in the excel sheet
read = False
while read == False:
    fileName = input("Enter the name of the file: ")
    try: 
        df = pd.read_excel(fileName)
        read = True
    except FileNotFoundError:
        print("File not found, please enter the correct name of the file.")

# replace all NaN with 0
df.fillna(0, inplace=True)
# Attempt to cycle through and print each player
for index in df.index:
    # Get the stats for each player
    stats = []
    weeks_attended = 0
    for i in range(10):
        stats.append(int(df.iloc[index, i+4])) # have to offset by 4 to account for avg's and week count infront of the weekly scores.
        if stats[i] != 0: weeks_attended += 1  # This is how we will count each player's total weeks attended.
    # calculate weekly average, then average of best 5.
    stats.sort(reverse=True)
    sum = weekly_avg = best_avg = 0.
    if weeks_attended == 0: continue
    for i in range(weeks_attended):
        sum += stats[i]
        if i <= 4:
            best_avg = sum
    # if weeks_attended == 0: continue
    weekly_avg = sum / weeks_attended
    if weeks_attended > 5:
        best_avg /= 5
    else:
        best_avg /= weeks_attended 
    # Add the data to the proper column
    df.loc[index, "Weekly Avg"] = round(weekly_avg, 1)
    df.loc[index, "Best 5 Weeks Avg"] = round(best_avg, 1)
    df.loc[index, "Weeks Attended"] = weeks_attended

# get the current week
week_number = int(df[['Weeks Attended']].max()[0])
# sort and export the results
sorted_df = df.sort_values(by=["Best 5 Weeks Avg", "Weekly Avg"], ascending=[False, False])
sorted_df.reset_index(inplace=True, drop=True)
sorted_df.index += 1
print(sorted_df)
output_str = "Week" +str(week_number) + "Results.xlsx"
sorted_df.to_excel(output_str)