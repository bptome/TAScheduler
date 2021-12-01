# Generated by Django 3.2.9 on 2021-12-01 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.IntegerField()),
                ('course_name', models.CharField(max_length=20)),
                ('instructor_id', models.IntegerField()),
                ('lab', models.CharField(max_length=20)),
                ('meeting_time', models.CharField(max_length=20)),
                ('semester', models.CharField(max_length=20)),
                ('course_type', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_id', models.IntegerField()),
                ('lab_name', models.CharField(max_length=20)),
                ('ta_id', models.IntegerField()),
                ('course_id', models.IntegerField()),
                ('has_grader', models.BooleanField()),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=1)),
                ('name', models.CharField(default='email', max_length=20)),
                ('password', models.CharField(default='email', max_length=20)),
                ('email', models.EmailField(default='email', max_length=20)),
                ('home_address', models.CharField(default='"101 W. Wisconsin Ave, Milwaukee, WI 53203"', max_length=20)),
                ('role', models.IntegerField(default=1)),
                ('phone', models.IntegerField(default=123)),
            ],
        ),
    ]
