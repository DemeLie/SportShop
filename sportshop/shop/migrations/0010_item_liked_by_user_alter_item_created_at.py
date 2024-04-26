# Generated by Django 5.0.4 on 2024-04-21 21:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_cartitem_quantity_alter_item_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='liked_by_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 21, 21, 35, 59, 720727, tzinfo=datetime.timezone.utc)),
        ),
    ]
