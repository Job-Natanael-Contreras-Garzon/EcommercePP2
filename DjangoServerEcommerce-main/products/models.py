from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        db_column='id_category',
        related_name='categories'
    )
    name = models.CharField(max_length=255)
    image1 = models.CharField(max_length=255, null=True)
    image2 = models.CharField(max_length=255, null=True)
    description = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'