# Generated by Django 4.2.16 on 2024-11-15 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inscripcion', '0035_curso_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscripcion',
            name='turno',
            field=models.ForeignKey(default='l', on_delete=django.db.models.deletion.CASCADE, related_name='turno', to='inscripcion.turno'),
        ),
    ]
