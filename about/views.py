from django.shortcuts import render

from backend.playermodel import PlayerModel
from backend.visualize import visualize_density_graph
from backend.results import pitch_swing_prob

# Create your views here.

def splash(request):
    p = PlayerModel("Austin Riley", ["2015-09-08", "2021-09-09"], 'batter')
    graph = visualize_density_graph(pitch_swing_prob(p.get_player_df(True), ['FF']), p.get_player_df(True))
    return render(request, 'splash.html', {'chart': graph})