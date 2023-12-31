# Generated by Django 3.2.8 on 2022-11-03 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('park_app', '0007_patient_details_doctor_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=500)),
                ('Fo', models.CharField(max_length=200)),
                ('Flo', models.CharField(max_length=200)),
                ('Abs', models.CharField(max_length=200)),
                ('shimmer', models.CharField(max_length=200)),
                ('dB', models.CharField(max_length=200)),
                ('APO', models.CharField(max_length=200)),
                ('DDA', models.CharField(max_length=200)),
                ('HNR', models.CharField(max_length=200)),
                ('RPDE', models.CharField(max_length=200)),
                ('DFA', models.CharField(max_length=200)),
                ('Spread2', models.CharField(max_length=200)),
                ('Spread1', models.CharField(max_length=200)),
                ('D2', models.CharField(max_length=200)),
                ('PPE', models.CharField(max_length=200)),
                ('result', models.CharField(max_length=200)),
                ('dt', models.DateField(auto_now_add=True)),
                ('tm', models.TimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=200)),
                ('patient_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_patient', to='park_app.patient_details')),
            ],
        ),
    ]
