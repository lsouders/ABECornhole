import pandas as pd

class Players:

    @staticmethod
    def get_players():
        df = pd.read_csv('data/Players.csv')
        return df
    
    @staticmethod
    def add_player(name):
        df = Players.get_players()
        index = df['Index'].max() + 1
        new_row = pd.DataFrame({'Name': [name], 'Index': [index]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('data/Players.csv', index=False)
        return index
    
    @staticmethod
    def get_player(name):
        df = Players.get_players()
        index = df[df['Name'] == name]
        return index.iloc[0, 1] if len(index) > 0 else -1
  
# df = Players.get_players()
# print(df.head())

# players = pd.read_csv("ABE Cornhole - Spring League.csv")
# players = players[['Players']]
# players.dropna(subset=['Players'], inplace=True)
# players['Index'] = range(1, len(players)+1)
# players.rename(columns={'Players': 'Name'}, inplace=True)
# print(players[['Name', 'Index']].head())
# players.to_csv('data/Players.csv', index=False)