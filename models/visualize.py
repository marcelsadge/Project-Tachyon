import pandas as pd
import matplotlib.patches as pt
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

from io import BytesIO
import base64

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
    #plt.show()

def visualize_density_graph(tup, player_df):
    plt.switch_backend('AGG')
    df = tup[2]
    visualize_cols = df.drop('swing', axis = 1).columns
    df_test = pd.DataFrame(data = tup[0][1], columns = visualize_cols)
    probables = pd.DataFrame(data = tup[1].predict_proba(tup[0][1]), columns = ['take_prob', 'swing_prob'])
    df_test['swing_prob'] = probables['swing_prob']
    top_sz = player_df['sz_top'].mean()
    bot_sz = player_df['sz_bot'].mean()
    sz = pt.Rectangle((-0.70833, bot_sz), width = 17/12, height = (top_sz - bot_sz), fill = False)
    fig, ax = plt.subplots()
    ax.add_patch(sz)
    data = np.vstack([df_test['plate_x'], df_test['plate_z']])
    density = gaussian_kde(data)
    xgrid = np.linspace(-1.5, 1.5, 40)
    ygrid = np.linspace(1, 3.75, 40)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    graph = density.evaluate(np.vstack([Xgrid.ravel(), Ygrid.ravel()]))
    plt.imshow(graph.reshape(Xgrid.shape),
           origin='lower', aspect='auto',
           extent=[-1.5, 1.5, 1, 3.75],
           cmap='Reds')
    plt.colorbar()
    imgdata = BytesIO()
    fig.savefig(imgdata, format = 'png')
    imgdata.seek(0)
    img = imgdata.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode('utf-8')
    imgdata.close()
    return fig, graph

