# Generated by Django 4.1.2 on 2022-11-02 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comet_problem', '0004_problem_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='objective',
            name='bounds',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='objective',
            name='optimization',
            field=models.TextField(default='min'),
        ),
    ]
