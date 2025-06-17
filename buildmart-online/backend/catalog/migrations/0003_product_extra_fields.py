from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_product_code'),
        ('users', '0002_supplierprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='base_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='min_order_quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='product',
            name='shipping_availability',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='users.supplierprofile'),
        ),
    ]
