# Generated by Django 5.0.4 on 2024-04-07 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_rename_channelband_client_channel_band_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='interface',
            new_name='interface_name',
        ),
        migrations.AddField(
            model_name='client',
            name='client_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]