from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=50, unique=True, default=''),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['code'], name='catalog_pro_code_idx'),
        ),
    ]
