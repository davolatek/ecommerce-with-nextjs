# Generated by Django 4.0.6 on 2022-07-20 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_api', '0002_alter_productimage_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='', help_text='Upload Product Images', upload_to='images/', verbose_name='Images'),
        ),
    ]
