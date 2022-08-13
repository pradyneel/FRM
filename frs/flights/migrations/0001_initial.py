# Generated by Django 4.1 on 2022-08-13 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authenticate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_no', models.CharField(max_length=50)),
                ('flight_time', models.TimeField()),
                ('flight_seats', models.CharField(max_length=4)),
                ('flight_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.user')),
            ],
        ),
    ]