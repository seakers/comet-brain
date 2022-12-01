# Generated by Django 4.1.2 on 2022-12-01 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comet_assistant', '0003_dialoguehistory_cleared_dialoguehistory_more_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dialoguehistory',
            old_name='cleared',
            new_name='hidden',
        ),
        migrations.AddField(
            model_name='dialoguehistory',
            name='loading',
            field=models.BooleanField(default=False),
        ),
    ]