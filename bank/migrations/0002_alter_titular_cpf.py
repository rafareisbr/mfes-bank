# Generated by Django 4.0.2 on 2022-03-28 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titular',
            name='cpf',
            field=models.CharField(max_length=11),
        ),
    ]
