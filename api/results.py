import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pybaseball as pb
from sklearn.model_selection import train_test_split
import sklearn as sk

from api.model import PlayerModel

def query_pitch_type_swing_prob(player_df: PlayerModel, query: None) -> pd.DataFrame:
    model_cols = ['plate_x','plate_z','release_speed','p_throws','pfx_x','pfx_z','vx0','vy0','vz0',
        'strikes','balls','prev_pitch', 'swing']
    query_df = player_df[model_cols]
    model_df = pd.get_dummies(query_df, ['pitches_', 'pitch_type_'])
    dep = model_df['swing'].astype(int)
    ind = model_df.drop('swing', axis = 1).values
    x_train, x_test, y_train, y_test = train_test_split(ind, dep, test_size = 0.2, random_state = 0)
    pass

def query_pitch_type_pitcher(player_df: PlayerModel, query: None) -> pd.DataFrame:
    pass

def query_release_speed_batter(player_df: PlayerModel, query: None) -> pd.DataFrame:
    pass

def query_release_speed_pitcher(player_df: PlayerModel, query: None) -> pd.DataFrame:
    pass

def visualize_results():
    pass