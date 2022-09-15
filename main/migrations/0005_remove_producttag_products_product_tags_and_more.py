# Generated by Django 4.0.5 on 2022-09-15 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_productimage_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttag',
            name='products',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='main.producttag'),
        ),
        migrations.AlterField(
            model_name='producttag',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
