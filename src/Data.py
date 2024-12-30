import pandas as pd
from Players import Players as p
from Alias import Alias as a
import matplotlib.pyplot as plt

class Data:

    def getData():
        # filename = input("filename: ")
        filename = 'main.csv'
        df = pd.read_csv(f'data/{filename}')
        return df, filename
    
    def cleanData(df):
        # Basic cleansing
        df.dropna(axis=1, how='all', inplace=True)
        df.drop(columns=['GameID', 'GameName', 'PlayerUser', 'PlayerEmail'], inplace=True)
        df = df.round(2)

        # Replace Alias names with true player names
        # call to alias class to do this for entire working df (not on main df)
        df = a.replace_alias(df)
        
        return df
    
    # Export data to csv sheet
    @staticmethod
    def storeData(df, filename):
        main = pd.read_csv('data/main.csv')
        main = pd.concat([main, df], ignore_index=True)
        main.to_csv(f'data/{filename}', index=False)

    # Throwaway: Code works as standalone, needs refactor to work as function
    def read_a_season():
        main = pd.read_csv('data/data_S24_W1.csv')
        main = Data.cleanData(main)
        main['Week'] = 1
        for i in range(2, 11):
            df = pd.read_csv(f'data/data_S24_W{i}.csv')
            df = Data.cleanData(df)
            df['Week'] = i
            main = pd.concat([main, df])
        main['Season'] = "Spring24"
        # print(f"Shape: {main.shape}\n")
        main.reset_index(drop=True, inplace=True)
        # print(main)
        Data.storeData(main, 'main.csv')

    # Throwaway: Code works as standalone, needs refactor to work as function
    def read_playoffs():
        main1 = pd.read_csv('data/W24_W11_A.csv')
        main1 = Data.cleanData(main1)
        main1['Week'] = 11

        main2 = pd.read_csv('data/W24_W11_B.csv')
        main2 = Data.cleanData(main2)
        main2['Week'] = 11

        main3 = pd.read_csv('data/W24_W11_C.csv')
        main3 = Data.cleanData(main3)
        main3['Week'] = 11

        main = pd.concat([main1, main2, main3])
        main['Season'] = 'Winter24'
        main.reset_index(drop=True, inplace=True)
        # print(main)
        Data.storeData(main, 'main.csv')

    def read_a_week(season, week, sort_num):
        df = pd.read_csv('data/data.csv')
        df = Data.cleanData(df)
        df['Week'] = week
        df['Season'] = season
        df['Season Sort'] = sort_num
        Data.storeData(df, 'main.csv')

    def graph(player_name, option='Player PPR', season='all'):
        df, _ = Data.getData()
        player_df = df[df['PlayerName'] == player_name]
        # Filter out a season if specified
        if season != 'all':
            player_df = player_df[player_df['Season'] == season]
        # Sort the data for graphing
        df = player_df.sort_values(by=['Season', 'Week'])
        if season == 'all': x_vals = list( range(1, len(df)+1) )
        else: x_vals = df['Week'].values
        plt.plot(x_vals, df[option])
        plt.xlabel('Week')
        plt.ylabel(option)
        plt.title(f'{player_name} {option} Stats for Season: {season}')
        plt.show()

    def get_stats(player_name, season='all'):
        df, _ = Data.getData()
        player_df = df[df['PlayerName'] == player_name]
        if season != 'all': player_df = player_df[player_df['Season'] == season]
        stats = {'Total Rounds': 0, 'Total Bags': 0, 'Total Points': 0, 'Total Opp Points': 0, 'Player PPR': 0, 'Opponent PPR': 0, '4in Total': 0, '4in PCT': 0, 'Total In': 0, 'In PCT': 0, 'Total On': 0, 'On PCT': 0, 'Total Off': 0, 'Off PCT': 0}
        # Total Rounds
        stats['Total Rounds'] = player_df['Rounds'].sum()
        # Total Bags
        stats['Total Bags'] = player_df['Bags'].sum()
        # Total Points
        stats['Total Points'] = player_df['Total Points'].sum()
        # Total Opp Points
        stats['Total Opp Points'] = player_df['Total Opp Points'].sum()
        # Player PPR
        stats['Player PPR'] = round( stats['Total Points'] / stats['Total Rounds'], 2 )
        # Opponent PPR
        stats['Opponent PPR'] = round( stats['Total Opp Points'] / stats['Total Rounds'], 2 )
        # 4in Total
        stats['4in Total'] = player_df['4In Count'].sum()
        # 4in PCT
        stats['4in PCT'] = round( stats['4in Total'] / stats['Total Rounds'], 3) * 100
        # Total In
        stats['Total In'] = player_df['In Count'].sum()
        # In PCT
        stats['In PCT'] = round( stats['Total In'] / stats['Total Bags'], 3) * 100
        # Total On (is bags in included in on??)
        stats['Total On'] = player_df['On Count'].sum()
        # On PCT
        stats['On PCT'] = round( stats['Total On'] / stats['Total Bags'], 3) * 100
        # Total Off
        stats['Total Off'] = player_df['Off Count'].sum()
        # Off PCT
        stats['Off PCT'] = round( stats['Total Off'] / stats['Total Bags'], 3) * 100
        
        results_df = pd.DataFrame(data=stats, index=[0])
        print(results_df)