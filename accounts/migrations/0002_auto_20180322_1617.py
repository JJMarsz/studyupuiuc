# Generated by Django 2.0.3 on 2018-03-22 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrolledIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('netID', models.TextField()),
                ('class_code', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='enrolledin',
            unique_together={('netID', 'class_code')},
        ),
    ]