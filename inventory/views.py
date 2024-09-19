import uuid
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from store import models
from django.contrib import messages
from django.db.models import Sum,F
from django.db import transaction
from store.models import Player, Team, AuctionLogs


@login_required(login_url='login')
def dashboard(request):
    total_players = Player.objects.count()
    total_teams = Team.objects.count()
    total_players_left = Player.objects.filter(captain=False, team_id=None).count()
    players_list = Player.objects.filter(captain=False, team_id=None).all()
    teams_list = Team.objects.all()
    context = {
        'total_players': total_players,
        'total_teams': total_teams,
        'total_players_left': total_players_left,
        'players_list': players_list,
        'teams_list': teams_list
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@require_POST
def add_player_to_team(request):
    player_id = request.POST.get('player_id')
    team_id = request.POST.get('team_id')
    price = request.POST.get('price')
    
    try:
        with transaction.atomic():
            if int(price) < 25000:
                messages.error(request, 'Invalid Price')
                return redirect('dashboard')
            # Get player and team objects
            player = Player.objects.get(id=player_id)
            team = Team.objects.get(id=team_id)

            # Calculate total spent on current players in the team
            player_team_comb = Player.objects.filter(team=team)
            team_player_count = player_team_comb.count()
            if team_player_count >= 12:
                messages.error(request, 'Your team is complete.')
                return redirect('dashboard')
            total_spent = player_team_comb.aggregate(total_price=Sum('price'))['total_price'] or 0
            remaining_players = 11 - team_player_count
            # import ipdb; ipdb.set_trace()
            # Team's total budget
            total_budget = 900000

            # Calculate remaining budget
            remaining_budget = total_budget - total_spent - int(price)

            # Minimum required budget for remaining players
            min_budget_for_remaining = remaining_players * 25000


            # Check if the remaining budget is enough to buy the remaining players
            if min_budget_for_remaining > remaining_budget:
                messages.error(request, 'Not enough budget to complete the team.')
                return redirect('dashboard')

            # If within budget, assign player to team and update price
            player.team = team
            player.price = int(price)
            player.save()
            # import ipdb; ipdb.set_trace()
            AuctionLogs.objects.update_or_create(
                player_order = player
            )

            # Success message
            messages.success(request, 'Player added to the team successfully!')
            return redirect('dashboard')

    except Player.DoesNotExist:
        # Handle error if player does not exist
        messages.error(request, 'Player does not exist.')
        return redirect('dashboard')

    except Team.DoesNotExist:
        # Handle error if team does not exist
        messages.error(request, 'Team does not exist.')
        return redirect('dashboard')
    
    except Exception as e:
        # Handle error if team does not exist
        messages.error(request, 'Error encountered.')
        return redirect('dashboard')



@login_required(login_url='login')
def get_tc_cobras_list(request):
    # import ipdb; ipdb.set_trace()
    team_obj = Team.objects.get(name='TC Cobras')
    team_list = Player.objects.filter(team=team_obj).all()
    total_budget = 900000
    total_spent = sum(player.price for player in team_list)
    remaining_budget = total_budget - total_spent
    context = {
        'team_obj': team_obj,
        'team_list': team_list,
        'remaining_budget': remaining_budget,  # Include remaining budget in context
        'total_spent': total_spent,  # Optionally, include total spent as well
        'remaining_players': 12 - team_list.count()
    }
    return render(request, 'store/tc_cobras.html', context)

@login_required(login_url='login')
def get_tc_eagles_list(request):
    team_obj = Team.objects.get(name='TC Eagles')
    team_list = Player.objects.filter(team=team_obj).all()
    total_budget = 900000
    total_spent = sum(player.price for player in team_list)
    remaining_budget = total_budget - total_spent
    context = {
        'team_obj': team_obj,
        'team_list': team_list,
        'remaining_budget': remaining_budget,  # Include remaining budget in context
        'total_spent': total_spent,  # Optionally, include total spent as well
        'remaining_players': 12 - team_list.count()
    }
    return render(request, 'store/tc_eagles.html', context)

@login_required(login_url='login')
def get_tc_hawks_list(request):
    team_obj = Team.objects.get(name='TC Hawks')
    team_list = Player.objects.filter(team=team_obj).all()
    total_budget = 900000
    total_spent = sum(player.price for player in team_list)
    remaining_budget = total_budget - total_spent
    context = {
        'team_obj': team_obj,
        'team_list': team_list,
        'remaining_budget': remaining_budget,  # Include remaining budget in context
        'total_spent': total_spent,  # Optionally, include total spent as well
        'remaining_players': 12 - team_list.count()
    }
    return render(request, 'store/tc_hawks.html', context)

@login_required(login_url='login')
def history(request):
    all_logs = AuctionLogs.objects.values(
        "created_at",
        player_name=F("player_order__name"),
        player_price=F("player_order__price"),
        team_name=F("player_order__team__name")
    ).order_by("created_at").all()
    context = {
        'logs': all_logs,
    }
    return render(request, 'store/auction_history.html', context)

@login_required(login_url='login')
def generate_random_player(request):
    unsold_players = Player.objects.filter(team__isnull=True)  # Players without a team
    print(unsold_players)
    return render(request, 'store/generate_random_player.html', {'players': unsold_players})