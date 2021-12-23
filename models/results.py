import pandas as pd
import sklearn as sk
import lightgbm as lgb
from sklearn.model_selection import train_test_split

# Preparing data for training
def pitch_swing_prob(player_df, pitches: None) -> pd.DataFrame:
    query_df = player_df.copy()
    l = []
    # We want the previous pitch to be one of our features
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
    # The dataset had mixed datatypes so we want to convert them all to int
    query_df['balls'] = query_df['balls'].astype(int)
    query_df['strikes'] = query_df['strikes'].astype(int)
    # Only getting pitches that we want
    query_df = query_df.loc[query_df['pitch_type'].isin(pitches)]
    query_df = query_df.iloc[::-1].reset_index(drop = True)
    # Dropping unimportant values
    query_df = query_df.drop(columns = ['pitch_type', 'pitch_number'])
    # One hot encode our features
    model_df = pd.get_dummies(query_df, ['pitches_', 'pitch_type_'])
    dep = model_df['swing'].astype(int)
    ind = model_df.drop('swing', axis = 1).values
    x_train, x_test, y_train, y_test = train_test_split(ind, dep, test_size = 0.2, random_state = 0)
    train_tup = x_train, x_test, y_train, y_test, model_df
    return train_on_classifier(train_tup)

# Uses the LGBMClassifier to train on the dataset to get a list of predictions. The default 
# values are optimal to obtain the highest accuracy. Other classifiers had low accuracy results.
# Returns a tuple containing all the information from the classification
def train_on_classifier(tup, lr = 0.9, max_depth = 20, num_leaves = 30, n_estimators = 150) -> tuple:
    x_train, x_test, y_train, y_test, df = tup[0], tup[1], tup[2], tup[3], tup[4]
    lgbm = lgb.LGBMClassifier(boosting_type = 'gbdt', objective = 'binary', 
    learning_rate = lr, max_depth = max_depth, num_leaves = num_leaves, n_estimators = n_estimators)
    lgbm.fit(x_train, y_train)
    prediction = lgbm.predict(x_test)
    accuracy = sk.metrics.accuracy_score(prediction, y_test)
    tup = ((x_train, x_test, y_train, y_test), lgbm, df, prediction, accuracy)
    return tup
    