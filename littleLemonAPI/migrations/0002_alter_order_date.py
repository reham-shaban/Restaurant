# Generated by Django 4.2.4 on 2023-08-30 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('littleLemonAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
    ]
