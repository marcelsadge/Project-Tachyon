import pybaseball as pb
import results, visualize

class PlayerModel(object):

    def __init__(self, player, year, type):
        self.player = self.simplify_player(player)
        self.year = year
        self.type = type
        self.raw_player_df = self.search(player = self.player, year = self.year)
        self.cleaned_player_df = self.clean(self.raw_player_df)
        self.data = None

    def __eq__(self, playermodel):
        if self.year != playermodel.year or self.type != playermodel.type:
            return False
        return True

    def __len__(self):
        return len(self.cleaned_player_df)

    def __deepcopy__(self):
        return PlayerModel(self.player, self.year, self.type)

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
        
    def simplify_player(self, player) -> tuple:
        player = player.lower()
        player_list = player.split()
        player_tup = (player_list[1], player_list[0])
        return player_tup

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

if __name__ == "__main__":
    p = PlayerModel("Austin Riley", ["2015-09-08", "2021-09-09"], 'batter')
    visualize.visualize_density_graph(results.pitch_swing_prob(
        p.get_player_df(True), ['FF']), p.get_player_df(True))

    p = PlayerModel("Clayton Kershaw", ["2015-09-08", "2021-09-09"], 'pitcher')
    visualize.visualize_density_graph(results.pitch_swing_prob(
        p.get_player_df(True), ['CU']), p.get_player_df(True))

