# Generated by Django 4.1.2 on 2023-02-02 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comet_problem', '0008_rename_objective_computedvalue_computed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computedvalue',
            name='value',
            field=models.TextField(),
        ),
    ]
