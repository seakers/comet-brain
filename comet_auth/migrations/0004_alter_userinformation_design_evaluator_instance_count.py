# Generated by Django 4.1.2 on 2022-10-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comet_auth', '0003_userinformation_design_evaluator_instance_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='design_evaluator_instance_count',
            field=models.IntegerField(default=10),
        ),
    ]
