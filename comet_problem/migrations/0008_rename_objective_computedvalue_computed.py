# Generated by Django 4.1.2 on 2023-02-01 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comet_problem', '0007_computed_aliases'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computedvalue',
            old_name='objective',
            new_name='computed',
        ),
    ]
