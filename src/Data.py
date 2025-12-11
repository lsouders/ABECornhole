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

    
    def read_data(filename, season, week, season_sort=4):
        df = pd.read_csv(filename)
        df = Data.cleanData(df)
        df['Week'] = week
        df['Season'] = season
        df['Season Sort'] = season_sort
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

    
    def get_rounds(season='all'):
        df, _ = Data.getData()
        if season != 'all':
            tmp = df[df['Season'] == season]
            df = tmp
        rounds = df.groupby('PlayerName')['Rounds'].sum().to_frame()
        rounds.sort_values('Rounds', ascending=False, inplace=True)

    
    def get_improvement(season='all'):
        df, _ = Data.getData()
        if season != 'all':
            tmp = df[df['Season'] == season]
            df  = tmp
        # df['Quality'] = 2 * df['In Percent'] + df['On Percent']
        df['Quality'] = df['Off Percent']
        first5 = df[(df['Week'] >= 1) & (df['Week'] <= 5)]
        last5  = df[(df['Week'] >= 6) & (df['Week'] <= 10)]

        first5_filtered = first5[first5.groupby('PlayerName')['PlayerName'].transform('count') >= 3]
        first5_quality = first5_filtered.groupby('PlayerName')['Quality'].mean().to_frame()
        first5_quality.rename(columns={'Quality': 'First 5 Quality'}, inplace=True)

        last5_filtered = last5[last5.groupby('PlayerName')['PlayerName'].transform('count') >= 3]
        last5_quality  = last5_filtered.groupby('PlayerName')['Quality'].mean().to_frame()
        last5_quality.rename(columns={'Quality': 'Last 5 Quality'}, inplace=True)

        df = pd.merge(first5_quality, last5_quality, on='PlayerName', how='inner')

        df['Improvement'] = df['First 5 Quality'] - df['Last 5 Quality']
        df.sort_values(by='Improvement', ascending=False, inplace=True)

        print(df)
    

    def build_season_master(season, append_file):
        master_df = pd.read_csv(f'{season}\\master.csv')
        append_df = pd.read_csv(f'{append_file}')
        result = pd.concat([master_df, append_df], ignore_index=True)
        pd.to_csv(f'{season}\\master.csv')


    def clear_season(season):
        filename = f'{season}\\{season}Main.csv'
        df = pd.read_csv(filename)
        df.loc[:, 'Best 5 Weeks Avg':] = 0
        df.to_csv(filename, index=False)