# Generated by Django 3.2.4 on 2022-10-11 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('hod', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('hof', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('matric_no', models.CharField(blank=True, max_length=50, null=True)),
                ('level', models.CharField(blank=True, choices=[('ND', 'ND'), ('HND', 'HND')], max_length=50, null=True)),
                ('program', models.CharField(blank=True, choices=[('PART-TIME', 'FULL-TIME')], max_length=50, null=True)),
                ('Faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.faculty')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.department')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(blank=True, max_length=6, null=True)),
                ('Faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.faculty')),
                ('Student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.student')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.department')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.faculty'),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('course_code', models.CharField(blank=True, max_length=6, null=True)),
                ('Faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.faculty')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin1.department')),
            ],
        ),
    ]
