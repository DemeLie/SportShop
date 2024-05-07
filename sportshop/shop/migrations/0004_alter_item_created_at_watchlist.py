# Generated by Django 5.0.4 on 2024-04-17 16:19

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_item_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 17, 16, 19, 18, 792866, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]