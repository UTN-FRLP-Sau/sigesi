# Generated by Django 4.2.16 on 2024-11-15 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscripcion', '0034_turno_alter_curso_modalidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='turno',
            field=models.ManyToManyField(to='inscripcion.turno'),
        ),
    ]
