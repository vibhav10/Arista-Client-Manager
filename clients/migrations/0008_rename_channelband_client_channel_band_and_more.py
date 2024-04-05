# Generated by Django 5.0.2 on 2024-04-05 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_rename_channel_band_client_channelband_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='channelband',
            new_name='channel_band',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='channelwidth',
            new_name='channel_width',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='clientLab',
            new_name='client_lab',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='clientPassword',
            new_name='client_password',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='clientPort',
            new_name='client_port',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='clientUsername',
            new_name='client_username',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='clientIP',
            new_name='ethernet_ip',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='status',
            new_name='ethernet_status',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='noisemeasurement',
            new_name='noise_measurement',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='ssidname',
            new_name='ssid_name',
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('ethernet_ip', 'client_port')},
        ),
        migrations.AddField(
            model_name='client',
            name='wifi_status',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='client',
            name='clientName',
        ),
        migrations.RemoveField(
            model_name='client',
            name='traffic_profile',
        ),
    ]