
import pandas as pd
from django.core.management import BaseCommand
from django.db import transaction

from store.models import Player, Team


class Command(BaseCommand):
    help = "upload players list from excel"

    def add_arguments(self, parser):
        parser.add_argument("--filepath", type=str, required=True)

    def handle(self, *args, **options):
        try:
            filepath = options["filepath"]
            self.update_teams_in_db(filepath)
            self.update_players_in_db(filepath)
            print("SUCCESSFULLY DONE.")
        except Exception as e:
            print(e)
            print(self.style.ERROR(f"ERROR: {str(e)}"))

    def update_teams_in_db(self, filepath):
        print("STARTING TO UPDATE TEAMS LIST")
        with transaction.atomic():
            # Read the excel file
            df = pd.read_excel(filepath, sheet_name="Teams")
            # Iterate over the rows
            for index, row in df.iterrows():
                team, created = Team.objects.get_or_create(
                    name=row["Team Name"],
                    defaults={
                        "budget": row["Budget"],
                        "max_players": row["Team Size"],
                    },
                )
                if not created:
                    team.budget = row["Budget"]
                    team.max_players = row["Team Size"]
                    team.save()
            print("Teams list updated successfully.")
            return True
        return False

    def update_players_in_db(self, filepath):
        print("STARTING TO UPDATE PLAYERS LIST")
        with transaction.atomic():
            # Read the excel file
            # import ipdb; ipdb.set_trace()
            df = pd.read_excel(filepath, sheet_name="Players")
            # Iterate over the rows
            for index, row in df.iterrows():
                is_captain=row["Captain"]
                player = Player.objects.create(
                    name=row["Player"],
                    player_id=index+1,
                    price=0,
                    captain=is_captain,
                    team=Team.objects.get(name=row["Captain Team Name"]) if is_captain else None,
                    profile=row["CricHeroes Profile"],
                    category=str(row["Category"]) + " " + "Set " + str(row["Tag"]),
                )
                player.save()
            print("Players list updated successfully.")
            return True
        return False
