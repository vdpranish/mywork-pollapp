# Generated by Django 3.1 on 2020-09-15 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_uploadpdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadpdf',
            name='pdf_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]