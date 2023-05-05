from django.db import migrations
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [
        ('onlineStore', '0002_rename_product_id_products_id_and_more'),
    ]

    # operations = [
    #     migrations.RunPython(set_cart_product_type_default),
    # ]
    atomic = False



