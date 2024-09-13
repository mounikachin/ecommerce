# Generated by Django 4.2.7 on 2023-12-22 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_profile_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name_plural': 'Team Table'},
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='categories'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(upload_to='dishes'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profiles'),
        ),
    ]
