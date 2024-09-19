import uuid
from django.db import models

from users.models import User


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Drop(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    sortno = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('decline', 'Decline'),
        ('approved', 'Approved'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('bulk', 'Bulk'),
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    design = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True)
    drop = models.ForeignKey(Drop, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.courier_name

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    budget = models.IntegerField(default=100000000)  # Example budget field
    created_at = models.DateTimeField(auto_now_add=True)

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
    price = models.IntegerField(default=None)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)  # A player can belong to a team
    captain = models.BooleanField(default=False)  # Indicates if the player is a captain
    profile = models.CharField(max_length=1056, null=True, blank=True)

    class Meta:
        db_table = "player"
        ordering = ["id", "name"]
        indexes = [models.Index(fields=["name"])]
    
    def __str__(self):
        return "%s (%s)" % (self.__class__.__name__, self.id)

class AuctionLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player_order = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["id", "created_at"]
    
    def __str__(self):
        return "%s (%s)" % (self.__class__.__name__, self.id)
