# Generated by Django 3.0.5 on 2020-06-04 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('responder', '0002_responder_location'),
        ('reporter', '0019_incidentreport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentreport',
            name='responder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incidents', to='responder.Responder'),
        ),
    ]