# Generated by Django 3.1.1 on 2020-11-17 15:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_merge_20201117_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityPeriodRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeStatusRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('N', 'Negative'), ('P', 'Positive')], default='P', max_length=10)),
                ('num_of_days', models.PositiveIntegerField(default=30, validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(2)])),
                ('fired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ChangeThresholdRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.CharField(choices=[('B', 'Below threshold'), ('A', 'Above threshold'), ('O', 'On threshold')], default='A', max_length=20)),
                ('percentage_threshold', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(-100)])),
                ('fired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PriceThresholdRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.CharField(choices=[('B', 'Below threshold'), ('A', 'Above threshold'), ('O', 'On threshold')], default='A', max_length=20)),
                ('price_threshold', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(-100)])),
                ('fired', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendationAnalystRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='watchedstockrule',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='watchedstockrule',
            name='change_status',
        ),
        migrations.RemoveField(
            model_name='watchedstockrule',
            name='change_threshold',
        ),
        migrations.RemoveField(
            model_name='watchedstockrule',
            name='price_threshold',
        ),
        migrations.RemoveField(
            model_name='watchedstock',
            name='watched_stock_rule',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='ChangeStatus',
        ),
        migrations.DeleteModel(
            name='ChangeThreshold',
        ),
        migrations.DeleteModel(
            name='PriceThreshold',
        ),
        migrations.DeleteModel(
            name='WatchedStockRule',
        ),
        migrations.AddField(
            model_name='recommendationanalystrule',
            name='watched_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendation_analyst_rules', to='myapp.watchedstock'),
        ),
        migrations.AddField(
            model_name='pricethresholdrule',
            name='watched_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_threshold_rules', to='myapp.watchedstock'),
        ),
        migrations.AddField(
            model_name='changethresholdrule',
            name='watched_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_threshold_rules', to='myapp.watchedstock'),
        ),
        migrations.AddField(
            model_name='changestatusrule',
            name='watched_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='change_status_rules', to='myapp.watchedstock'),
        ),
        migrations.AddField(
            model_name='activityperiodrule',
            name='watched_stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_period_rules', to='myapp.watchedstock'),
        ),
    ]
