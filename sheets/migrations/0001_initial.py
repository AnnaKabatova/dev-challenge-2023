# Generated by Django 4.2.5 on 2023-09-28 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheet_id', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell_id', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('result', models.CharField(max_length=255, null=True)),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cell', to='sheets.sheet')),
            ],
        ),
    ]
