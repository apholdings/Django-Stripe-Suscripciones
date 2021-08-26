# Generated by Django 3.2.6 on 2021-08-19 15:05

import courses.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('stripe_price_id', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('currency', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='chapter',
            name='video',
            field=models.FileField(default=1, upload_to=courses.models.chapter_directory_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='video',
            field=models.FileField(default=1, upload_to=courses.models.user_directory_path),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video',
            field=models.FileField(default=1, upload_to=courses.models.lesson_directory_path),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stripe_subscription_id', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=100)),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='courses.pricing')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='pricing_tiers',
            field=models.ManyToManyField(blank=True, to='courses.Pricing'),
        ),
    ]
