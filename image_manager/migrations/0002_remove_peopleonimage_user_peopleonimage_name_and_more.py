# Generated by Django 4.0 on 2022-12-14 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peopleonimage',
            name='user',
        ),
        migrations.AddField(
            model_name='peopleonimage',
            name='name',
            field=models.CharField(default='Anonymous', max_length=255),
        ),
        migrations.AlterField(
            model_name='peopleonimage',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to='image_manager.image'),
        ),
    ]