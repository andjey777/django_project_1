# Generated by Django 4.1.3 on 2022-12-07 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0003_grapcard_grname_procrssor_procname_ram_ramname'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Procrssor',
            new_name='Processor',
        ),
    ]
