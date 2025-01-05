import pandas as pd
from Players import Players as p

class Alias:

    @staticmethod
    def get_alias():
        df = pd.read_csv('data/Alias.csv')
        return df
    
    @staticmethod
    def add_alias(player_name: str, index: int):
        df = Alias.get_alias()
        new_row = pd.DataFrame({'Alias': [player_name], 'Index': [index]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('data/Alias.csv', index=False)
    
    # Find a known alias for a given player (returns the index of that player)
    @staticmethod
    def get_alias_by_name(player_name):
        df = Alias.get_alias()
        index = df[df['Alias'] == player_name]
        return index.iloc[0, 1] if len(index) > 0 else -1 
    
    # Find a known alias for a given player (returns the Alias of that player)
    @staticmethod
    def get_alias_by_index(index) -> pd.DataFrame:
        df = Alias.get_alias()
        name = df[df['Index'] == index]
        return name if len(name) > 0 else -1 
    
    # Replace aliases with true names in dataframe that we plan to join to
    # the main dataframe.
    @staticmethod
    def replace_alias(df):
        # Get alias and player tables
        alias = Alias.get_alias()
        players = p.get_players()
        # Iterate over the df that we are cleaning
        for row in df.index:
            player_name = df.loc[row, 'PlayerName']
            known_alias = Alias.get_alias_by_name(player_name)
            # Alias does not exist, must add alias and possibly player
            if known_alias == -1:
                true_name = input(f'No alias found. Who is {player_name}?\nName: ')
                # Check if player exists
                index = p.get_player(true_name)
                if index == -1:
                    index = p.add_player(true_name)
                Alias.add_alias(player_name, index)
            else:
                true_name = players[players['Index'] == known_alias].iloc[0, 0]
            # Replace the alias with the true name
            df.loc[row, 'PlayerName'] = true_name
        return df