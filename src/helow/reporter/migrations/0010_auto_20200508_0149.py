# Generated by Django 3.0.5 on 2020-05-08 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0009_auto_20200508_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentlocation',
            name='incident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='reporter.IncidentReport'),
        ),
    ]
