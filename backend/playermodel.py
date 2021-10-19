import pandas as pd
import pybaseball as pb

import results

class PlayerModel(object):

    def __init__(self, player, year):
        self.player = self.simplify_player(player)
        self.year = year
        self.raw_player_df = self.search(player = self.player, year = self.year)
        self.cleaned_player_df = self.clean(self.raw_player_df)
        self.time_interval = year

    def search(self, player, year):
        player_df = pb.playerid_lookup(player[0], player[1])
        if player_df.empty:
            return
        player_id = player_df['key_mlbam'][0]
        if len(year) == 1:
            player_data = pb.statcast_batter(year[0], player_id)
            return player_data
        else:
            player_data = pb.statcast_batter(year[0], year[1], player_id)
            return player_data

    def clean(self, df):
        df = df.dropna(axis= 'columns', how = 'all')
        df = df.loc[(df['plate_x'].notnull()) & (df['plate_z'].notnull())]
        df = df.loc[(df['pitch_type'].notnull()) & (df['release_speed'].notnull())]
        df['swing'] = 0
        df.loc[df['description'].isin(['hit_into_play', 'swinging_strike', 'swinging_strike_blocked', 
            'foul', 'hit_into_play_no_out', 'foul_tip', 'hit_into_play_score', 'foul_bunt', 
            'missed_bunt']), 'swing'] = 1
        df = df.iloc[::-1].reset_index(drop = True)
        return df
        
    def simplify_player(self, player) -> tuple:
        player = player.lower()
        player_list = player.split()
        player_tup = (player_list[1], player_list[0])
        return player_tup

    def get_player_name(self):
        return ' '.join(list(self.player))

    def get_player_df(self, f):
        if not f:
            return self.raw_player_df
        return self.cleaned_player_df

if __name__ == "__main__":
    p = PlayerModel("Austin Riley", ["2015-09-08", "2021-09-09"])
    results.visualize_swing_results(results.query_pitch_type_swing_prob(
        p.get_player_df(True), ['FF']), p.get_player_df(True))

