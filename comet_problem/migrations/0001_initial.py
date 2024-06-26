# Generated by Django 4.1.2 on 2022-10-20 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comet_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Architecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation', models.TextField()),
                ('evaluation_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('type', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet_problem.problem')),
                ('user_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet_auth.userinformation')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectiveValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('explanation', models.TextField()),
                ('architecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet_problem.architecture')),
                ('objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet_problem.objective')),
            ],
        ),
        migrations.AddField(
            model_name='objective',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet_problem.problem'),
        ),
        migrations.AddField(
            model_name='architecture',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet_problem.problem'),
        ),
        migrations.AddField(
            model_name='architecture',
            name='user_information',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comet_auth.userinformation'),
        ),
    ]
