import pandas as pd

class Players:

    @staticmethod
    def get_players() -> pd.DataFrame:
        df = pd.read_csv('data/Players.csv')
        return df
    
    @staticmethod
    def add_player(name: str) -> int:
        df = Players.get_players()
        index = df['Index'].max() + 1
        new_row = pd.DataFrame({'Name': [name], 'Index': [index]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('data/Players.csv', index=False)
        return index
    
    @staticmethod
    def get_player(name) -> int:
        df = Players.get_players()
        index = df[df['Name'] == name]
        return index.iloc[0, 1] if len(index) > 0 else -1
    
    @staticmethod
    def get_player_by_index(index: int) -> str:
        df = Players.get_players()
        name = df[df['Index'] == index]
        return name.iloc[0, 0] if len(name) > 0 else ''