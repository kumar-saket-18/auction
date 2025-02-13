import uuid
from django.db import models
from datetime import datetime

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    budget = models.IntegerField(default=900000)
    created_at = models.DateTimeField(auto_now_add=True)
    max_players = models.IntegerField(default=12)

    class Meta:
        db_table = "team"
        ordering = ["id", "name"]
        indexes = [models.Index(fields=["name"])]
    
    def __str__(self):
        return "%s (%s)" % (self.__class__.__name__, self.id)

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    player_id = models.IntegerField(default=None)
    price = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)  # A player can belong to a team
    captain = models.BooleanField(default=False)  # Indicates if the player is a captain
    profile = models.CharField(max_length=1056, null=True, blank=True)
    is_unsold = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=datetime.now())
    category = models.CharField(max_length=1056, null=True, blank=True)

    class Meta:
        db_table = "player"
        ordering = ["id", "name"]
        indexes = [models.Index(fields=["name"])]
    
    def __str__(self):
        return "%s (%s)" % (self.__class__.__name__, self.id)

class AuctionLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player_order = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=55, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["id", "created_at"]
    
    def __str__(self):
        return "%s (%s)" % (self.__class__.__name__, self.id)
