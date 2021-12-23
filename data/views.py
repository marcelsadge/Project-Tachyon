from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as log, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from matplotlib.pyplot import plot
from data.models import Account, Images
from django.core.files.images import ImageFile

from models.playermodel import PlayerModel
from models.visualize import visualize_density_graph
from models.results import pitch_swing_prob

import string, random, copy

# Splash page 
def splash(request):
    return render(request, 'home1.html')

# Home page 
def home(request):
    return render(request, 'home.html')

# Login page 
def login(request):
    return render(request, "login.html")

# Handles login through posts
def request_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if not username or not password:
        return redirect("/login")
    if user is None:
        return redirect("/login")
    else:
        log(request, user)
        Images.objects.all().delete()
        return redirect("/home/")

# Confirms if the user wants to logout
@login_required
def confirm_logout(request):
    return render(request, "confirmlogout.html")

# Logout method after the user confirms
@login_required
def request_logout(request):
    logout(request)
    return redirect("/")

# Register page
def register(request):
    return render(request, "register.html")

# Handles registering throught posts
def request_register(request):
    username = request.POST["username"]
    password = request.POST["password"]
    name = request.POST["name"]
    if not username or not password or not name:
        return redirect('/register')
    if not Account.objects.filter(user__username=username):
        user = User.objects.create(username=username, password=password)
        user.set_password(password)
        user.save()
        Account.objects.create(user=user, name=name)
        log(request, user)
        Images.objects.all().delete()
        return redirect('/home')
    else:
        return redirect('/register')

# Handles profile information
def profile_account(request, username):
    if not User.objects.get(username=username):
        return render("Error use not found.")
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)
    images = Images.objects.filter(user=user)
    return render(request, "profile.html",
    {
        "accounts": account, 
        "users": user,
        "images": images
    })

# Search page
def search(request):
    return render(request, "search.html")

# Handles player search through posts and creates image model for account
def create_query(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date1 = request.POST['date1']
        date2 = request.POST['date2']
        type = request.POST['type']
        pitches = request.POST['pitches']
        pname = first_name + " " + last_name
        type = type.lower()
        l = copy.copy(pitches)
        pitches = pitches.split(" ")
        if not first_name or not last_name or not date1 or not date2 or not type or not pitches:
            return redirect('/search')
        p = PlayerModel(player = pname, year = (date1, date2), type = type)
        graph = None
        fig, graph = visualize_density_graph(pitch_swing_prob(p.get_player_df(True), pitches), p.get_player_df(True))
        
        letters = string.ascii_lowercase
        file = ''.join(random.choice(letters) for i in range(10)) + '.png'
        fig.savefig('static/'+ file)
        loc = file
        plot_instance = Images.objects.create(
            account = Account.objects.get(user=request.user),
            user = request.user,
            name = pname,
            date1 = date1,
            date2 = date2,
            type = type, 
            pitches = l,
            img = loc)
        plot_instance.save()
    return render(request, 'player.html', {'chart': graph, 'pname': pname, 'date1': date1, 'date2': date2, 'pitches': l})  
