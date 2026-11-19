from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

 
class Product(models.Model):
    description = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)

    class Meta:
        ordering = ["description"]

    def __str__(self):
        return self.description
