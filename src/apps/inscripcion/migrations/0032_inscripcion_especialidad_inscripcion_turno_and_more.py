# Generated by Django 4.2.16 on 2024-11-13 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inscripcion', '0031_curso_inscripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripcion',
            name='especialidad',
            field=models.IntegerField(choices=[(5, 'Ing. en Sistemas de Informacion'), (7, 'Ing. en Energia Electrica'), (17, 'Ing. Mecanica'), (24, 'Ing. Industrial'), (27, 'Ing. Quimica'), (31, 'Ing. Civil')], db_column='especialidad', default='31'),
        ),
        migrations.AddField(
            model_name='inscripcion',
            name='turno',
            field=models.CharField(choices=[('m', 'Turno Mañana'), ('t', 'Turno Tarde'), ('n', 'Turno Noche')], db_column='turno', default='t', max_length=1),
        ),
        migrations.AlterField(
            model_name='inscripcion',
            name='modalidad',
            field=models.ForeignKey(default='l', on_delete=django.db.models.deletion.CASCADE, related_name='modalidad', to='inscripcion.modalidadcursado'),
        ),
    ]
