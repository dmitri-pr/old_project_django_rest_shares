# Generated by Django 4.1.5 on 2023-08-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsanalyzing', '0002_alter_parsanalyzing_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parsanalyzing',
            old_name='forw_price',
            new_name='sfrw_price',
        ),
        migrations.AddField(
            model_name='parsanalyzing',
            name='lfrw_price',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
