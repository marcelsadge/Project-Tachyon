import pandas as pd
import numpy as np
from matplotlib import cm
import matplotlib.patches as pt
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import pybaseball as pb
from sklearn.model_selection import train_test_split
import sklearn as sk
import seaborn as se

import lightgbm as lgb

import playermodel as pm

def pitch_swing_prob(player_df, pitches: None) -> pd.DataFrame:
    query_df = player_df.copy()
    l = []
    for i in range(len(query_df)):
        prev_pitch = None
        if query_df['pitch_number'][i] == 1:
            prev_pitch = 'NA'
        elif query_df['pitch_number'][i] != 1:
            prev_pitch = query_df['pitch_type'][i - 1]
        l.append(prev_pitch)
    query_df['prev_pitch_type'] = l
    model_cols = ['pitch_type', 'prev_pitch_type', 'pitch_number', 'plate_x','plate_z',
        'release_speed','p_throws','pfx_x','pfx_z','vx0','vy0','vz0',
        'strikes','balls', 'swing']
    query_df = query_df[model_cols]
    query_df['balls'] = query_df['balls'].astype(int)
    query_df['strikes'] = query_df['strikes'].astype(int)
    query_df = query_df.loc[query_df['pitch_type'].isin(pitches)]
    query_df = query_df.iloc[::-1].reset_index(drop = True)
    query_df = query_df.drop(columns = ['pitch_type', 'pitch_number'])
    model_df = pd.get_dummies(query_df, ['pitches_', 'pitch_type_'])
    dep = model_df['swing'].astype(int)
    ind = model_df.drop('swing', axis = 1).values
    x_train, x_test, y_train, y_test = train_test_split(ind, dep, test_size = 0.2, random_state = 0)
    train_tup = x_train, x_test, y_train, y_test, model_df
    return train_on_classifier(train_tup)

def query_release_speed_batter(player_df, query: None) -> pd.DataFrame:
    pass

def query_release_speed_pitcher(player_df, query: None) -> pd.DataFrame:
    pass

def train_on_classifier(tup, lr = 0.9, max_depth = 20, num_leaves = 30, n_estimators = 150) -> tuple:
    x_train, x_test, y_train, y_test, df = tup[0], tup[1], tup[2], tup[3], tup[4]
    lgbm = lgb.LGBMClassifier(boosting_type = 'gbdt', objective = 'binary', 
    learning_rate = lr, max_depth = max_depth, num_leaves = num_leaves, n_estimators = n_estimators)
    lgbm.fit(x_train, y_train)
    prediction = lgbm.predict(x_test)
    accuracy = sk.metrics.accuracy_score(prediction, y_test)
    tup = ((x_train, x_test, y_train, y_test), lgbm, df, prediction, accuracy)
    return tup


def visualize_swing_prob(tup, player_df):
    df = tup[2]
    visualize_cols = df.drop('swing', axis = 1).columns
    df_test = pd.DataFrame(data = tup[0][1], columns = visualize_cols)
    probables = pd.DataFrame(data = tup[1].predict_proba(tup[0][1]), columns = ['take_prob', 'swing_prob'])
    df_test['swing_prob'] = probables['swing_prob']
    top_sz = player_df['sz_top'].mean()
    bot_sz = player_df['sz_bot'].mean()
    sz = pt.Rectangle((-0.70833, bot_sz), width = 17/12, height = (top_sz - bot_sz), fill = False)
    _, ax = plt.subplots()
    ax.add_patch(sz)
    ax.axis('equal')
    plt.hist2d(df_test['plate_x'], df_test['plate_z'], bins = 30, cmap = 'Reds')
    plt.colorbar()
    plt.xlim(-1.5, 1.5)
    plt.ylim(1, 3.75)
    plt.show()


