# Generated by Django 3.1.13 on 2024-09-19 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20240916_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='drop',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='season',
        ),
        migrations.RemoveField(
            model_name='order',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='user',
        ),
        migrations.AddField(
            model_name='player',
            name='is_unsold',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='team',
            name='budget',
            field=models.IntegerField(default=900000),
        ),
        migrations.DeleteModel(
            name='Buyer',
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
        migrations.DeleteModel(
            name='Drop',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Season',
        ),
        migrations.DeleteModel(
            name='Supplier',
        ),
    ]
