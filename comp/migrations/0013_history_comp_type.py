# Generated by Django 4.1.3 on 2023-04-05 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0012_rename_grap_card_res_history_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='comp_type',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]