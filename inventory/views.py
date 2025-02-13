from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from inventory.constants import AppConstants, ErrorStrings, AuctionLogsActionEnum, SuccessMessages
from store import models
from django.contrib import messages
from django.db.models import Sum,F
from django.db import transaction
from datetime import datetime
from store.models import Player, Team, AuctionLogs


@login_required(login_url='login')
def dashboard(request):
    total_players_registered_for_auction = Player.objects.filter(captain=False).count()
    total_teams = Team.objects.count()
    total_players_remaining_for_auction = Player.objects.filter(captain=False, team_id=None, is_unsold=False).count()
    total_players_unsold = Player.objects.filter(captain=False, team_id=None, is_unsold=True).count()
    players_list_to_be_auctioned = Player.objects.filter(captain=False, team_id=None).order_by("player_id")
    teams_list = Team.objects.all()

    context = {
        'total_players_registered_for_auction': total_players_registered_for_auction,
        'total_teams': total_teams,
        'total_players_remaining_for_auction': total_players_remaining_for_auction,
        'total_players_unsold': total_players_unsold,
        'players_list': players_list_to_be_auctioned,
        'teams_list': teams_list
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
@require_POST
def add_player_to_team(request):
    player_id = request.POST.get('player_id')
    team_id = request.POST.get('team_id')
    price = request.POST.get('price')

    if not player_id or not team_id or not price:
        messages.error(request, ErrorStrings.MISSING_PARAMETERS)
        return redirect('dashboard')

    try:
        price = int(price)
        if price < AppConstants.MIN_PRICE:
            messages.error(request, ErrorStrings.INVALID_PRICE)
            return redirect('dashboard')

        with transaction.atomic():
            # Get player and team objects
            player = get_object_or_404(Player, id=player_id)
            team = get_object_or_404(Team, id=team_id)

            team_players = Player.objects.filter(team=team)
            team_player_count = team_players.count()

            if team_player_count >= team.max_players:
                messages.error(request, ErrorStrings.TEAM_FULL)
                return redirect('dashboard')

            # Calculate total spent on the team
            total_spent = team_players.aggregate(total_price=Sum('price'))['total_price'] or 0
            remaining_players = (team.max_players - 1) - team_player_count

            # Calculate remaining budget
            remaining_budget = team.budget - total_spent - price
            min_budget_required = remaining_players * AppConstants.MIN_PRICE

            if remaining_budget < min_budget_required:
                messages.error(request, ErrorStrings.INSUFFICIENT_BUDGET)
                return redirect('dashboard')

            # Assign player to the team
            player.team = team
            player.price = price
            player.updated_at = datetime.now()
            player.save()

            AuctionLogs.objects.update_or_create(
                player_order=player,
                action=AuctionLogsActionEnum.SOLD.value
            )

            messages.success(request, SuccessMessages.PLAYER_ADDED)
            return redirect('dashboard')

    except ValueError:
        messages.error(request, ErrorStrings.INVALID_PRICE_FORMAT)
        return redirect('dashboard')

    except Exception as e:
        messages.error(request, ErrorStrings.GENERIC_ERROR)
        return redirect('dashboard')



@login_required(login_url='login')
def get_tc_falcons_list(request):
    team_obj = get_object_or_404(Team, name='TC Falcons')

    team_list = Player.objects.filter(team=team_obj).order_by("updated_at")
    total_spent = team_list.aggregate(total_spent=Sum('price'))['total_spent'] or 0
    remaining_budget = team_obj.budget - total_spent

    context = {
        'team_obj': team_obj,
        'team_list': team_list,
        'remaining_budget': remaining_budget,
        'total_spent': total_spent,
        'remaining_players': team_obj.max_players - team_list.count()
    }
    return render(request, 'store/tc_falcons.html', context)


@login_required(login_url='login')
def get_tc_eagles_list(request):
    team_obj = get_object_or_404(Team, name='TC Eagles')

    team_list = Player.objects.filter(team=team_obj).order_by("updated_at")
    total_spent = team_list.aggregate(total_spent=Sum('price'))['total_spent'] or 0
    remaining_budget = team_obj.budget - total_spent

    context = {
        'team_obj': team_obj,
        'team_list': team_list,
        'remaining_budget': remaining_budget,
        'total_spent': total_spent,
        'remaining_players': team_obj.max_players - team_list.count()
    }
    return render(request, 'store/tc_eagles.html', context)


@login_required(login_url='login')
def get_tc_hawks_list(request):
    team_obj = get_object_or_404(Team, name='TC Hawks')
    
    team_list = Player.objects.filter(team=team_obj).order_by("updated_at")
    total_spent = team_list.aggregate(total_spent=Sum('price'))['total_spent'] or 0
    remaining_budget = team_obj.budget - total_spent

    context = {
        'team_obj': team_obj,
        'team_list': team_list,
        'remaining_budget': remaining_budget,
        'total_spent': total_spent,
        'remaining_players': team_obj.max_players - team_list.count()
    }
    return render(request, 'store/tc_hawks.html', context)


@login_required(login_url='login')
def history(request):
    all_logs = AuctionLogs.objects.values(
        "created_at",
        "action",
        player_name=F("player_order__name"),
        player_price=F("player_order__price"),
        team_name=F("player_order__team__name")
    ).order_by("-created_at").all()
    context = {
        'logs': all_logs,
    }
    return render(request, 'store/auction_history.html', context)

@login_required(login_url='login')
def generate_random_player(request):

    players = Player.objects.filter(team__isnull=True, is_unsold=False).order_by("category","player_id")

    # Group players by category
    categorized_players = {}
    for player in players:
        category = player.category or "Uncategorized"
        if category not in categorized_players:
            categorized_players[category] = []
        categorized_players[category].append(player)

    return render(request, 'store/generate_random_player.html', {'categorized_players': categorized_players})

@login_required(login_url='login')
def generate_random_unsold_player(request):
    unsold_players = Player.objects.filter(team__isnull=True, is_unsold=True).order_by("category","player_id")  # Players without a team
    return render(request, 'store/generate_random_unsold_players.html', {'players': unsold_players})

@login_required(login_url='login')
def mark_unsold(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        if not player_id:
            messages.error(request, ErrorStrings.MISSING_PLAYER_ID)
            return redirect('dashboard')
        
        player = get_object_or_404(Player, id=player_id)
        player.is_unsold = True
        player.updated_at = datetime.now()
        player.save()

        AuctionLogs.objects.update_or_create(
            player_order=player,
            defaults={"action": AuctionLogsActionEnum.UNSOLD.value}
        )

        messages.success(request, SuccessMessages.PLAYER_MARKED_UNSOLD)
    return redirect('dashboard')