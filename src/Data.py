import pandas as pd
from Players import Players as p
from Alias import Alias as a

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