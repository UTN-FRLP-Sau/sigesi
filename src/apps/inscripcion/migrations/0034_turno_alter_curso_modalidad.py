# Generated by Django 4.2.16 on 2024-11-15 15:05

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscripcion', '0033_alter_curso_periodo_cierre_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Turno',
                'verbose_name_plural': 'Turnos',
            },
        ),
    ]
