import pybaseball as pb

# The PlayerModel uses the pybaseball library to query specific players 
# depending on their name and dates. The output is a cleaned dataframe
# on all the important stats.
class PlayerModel(object):

    def __init__(self, player, year, type):
        self.player = self.simplify_player(player)
        self.year = year
        self.type = type
        self.raw_player_df = self.search(player = self.player, year = self.year)
        self.cleaned_player_df = self.clean(self.raw_player_df)
        self.data = None

    # Checks if query was made already
    def __eq__(self, playermodel):
        if self.year != playermodel.year or self.type != playermodel.type:
            return False
        return True

    # Checks if the dataframe is empty
    def __len__(self):
        return len(self.cleaned_player_df)

    # Makes a copy of model
    def __deepcopy__(self):
        return PlayerModel(self.player, self.year, self.type)

    # Searches a player's id through playerid_lookup() before
    # querying their data. Pitcher or batter must be defined
    # as the dataframes are different between the two.
    def search(self, player, year):
        player_df = pb.playerid_lookup(player[0], player[1])
        if player_df.empty:
            return
        player_id = player_df['key_mlbam'][0]
        player_data = None
        if len(year) == 1:
            if self.get_type() == 'batter':
                player_data = pb.statcast_batter(year[0], player_id)
            elif self.get_type() == 'pitcher':
                player_data = pb.statcast_pitcher(year[0], player_id)
        else:
            if self.get_type() == 'batter':
                player_data = pb.statcast_batter(year[0], year[1], player_id)
            elif self.get_type() == 'pitcher':
                player_data = pb.statcast_pitcher(year[0], year[1], player_id)
        return player_data

    # Cleans the dataframe for pitches swung at or called for strikes for 
    # batters and pitchers respectively
    def clean(self, df):
        df = df.dropna(axis= 'columns', how = 'all')
        df = df.loc[(df['plate_x'].notnull()) & (df['plate_z'].notnull())]
        df = df.loc[(df['pitch_type'].notnull()) & (df['release_speed'].notnull())]
        df['swing'] = 0
        if self.get_type() == 'batter':
            df.loc[df['description'].isin(['hit_into_play', 'swinging_strike', 'swinging_strike_blocked', 
                'foul', 'hit_into_play_no_out', 'foul_tip', 'hit_into_play_score', 'foul_bunt', 
                'missed_bunt']), 'swing'] = 1
        elif self.get_type() == 'pitcher':
            df.loc[df['description'].isin(['hit_into_play', 'called_strike', 'swinging_strike', 'swinging_strike_blocked', 
            'foul', 'foul_tip', 'hit_into_play', 'foul_bunt', 
            'missed_bunt']), 'swing'] = 1
        df = df.iloc[::-1].reset_index(drop = True)
        return df
    
    # Make the inputs lowercase
    def simplify_player(self, player) -> tuple:
        player = player.lower()
        player_list = player.split()
        player_tup = (player_list[1], player_list[0])
        return player_tup

    # Setters and getters below
    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_type(self):
        return self.type

    def get_player_name(self):
        return ' '.join(list(self.player))

    def get_player_df(self, f):
        if not f:
            return self.raw_player_df
        return self.cleaned_player_df
