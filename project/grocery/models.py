from django.db import models


class Category(models.Model):
    red_circle_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    has_children = models.BooleanField(default=False)
    is_root = models.BooleanField(default=False)
    path = models.CharField(max_length=255)
    link = models.URLField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True
        )
    red_circle_parent_id = models.CharField(max_length=255, null=True, default=None)
    parent_name = models.CharField(max_length=255, null=True, default=None)
    type = models.CharField(max_length=50)
    domain = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    red_circle_product_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    cost = models.FloatField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    unit_cost = models.FloatField(null=False, blank=False)
    unit_price = models.FloatField(null=False, blank=False)
    size = models.FloatField(null=True)
    category = models.ForeignKey("grocery.Category", on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='sub_category'
    )
    image = models.URLField(blank=True, null=True)
    brand = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ingredients = models.CharField(max_length=255, null=True, blank=True, default=None)
    source = models.CharField(max_length=255, default="Red Circle API")

    def __str__(self):
        return self.title
