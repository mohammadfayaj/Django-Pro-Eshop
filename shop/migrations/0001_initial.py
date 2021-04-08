# Generated by Django 3.1.7 on 2021-04-08 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_pic')),
                ('slug', models.SlugField(help_text='Unique value for product page URL, created from name.', unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titel', models.CharField(max_length=100, null=True)),
                ('images', models.ImageField(upload_to='productitem_pic')),
                ('images_1', models.ImageField(blank=True, null=True, upload_to='productitem_pic')),
                ('images_2', models.ImageField(blank=True, null=True, upload_to='productitem_pic')),
                ('images_3', models.ImageField(blank=True, null=True, upload_to='productitem_pic')),
                ('meta_keywords', models.CharField(blank=True, help_text='Comma-delimited set of SEO keywords for meta tag', max_length=255, null=True, verbose_name='Meta keywords')),
                ('meta_description', models.CharField(blank=True, help_text='Content for description meta tag', max_length=255, null=True, verbose_name='Meta Description')),
                ('description', models.TextField(blank=True, null=True)),
                ('brand', models.CharField(blank=True, max_length=50, null=True)),
                ('availability', models.TextField(blank=True, choices=[('In stock', 'In stock'), ('Out of stock', 'Out Of Stock')], default='In stock', null=True)),
                ('colors', models.TextField(blank=True, choices=[('White', 'White'), ('Gray', 'Gray '), ('Red', 'Red'), ('Black', 'Black'), ('Green', 'Green'), ('Blue', 'Blue')], null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9)),
                ('is_active', models.BooleanField(default=True)),
                ('is_bestseller', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_it_shirt', models.BooleanField(default=False)),
                ('is_it_Shoes', models.BooleanField(default=False)),
                ('is_it_pant', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(help_text='How many product quantity do you have?', null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(default=uuid.uuid4, help_text='Unique value for product page URL, Auto genarated, But still if you want to Edit! You can.', null=True, unique=True)),
                ('categorys', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.category')),
            ],
            options={
                'verbose_name_plural': 'Product Items',
                'ordering': ['date_added'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=600)),
                ('image', models.ImageField(blank=True, null=True, upload_to='reviews_pic')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.reviews')),
                ('product_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productitem')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_pic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
            options={
                'verbose_name_plural': 'Product Reviews By Customer',
            },
        ),
    ]
