from django.db import models
from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    title = models.CharField(max_length=150)
    about = models.TextField(blank=True, null=True)
    price_14 = models.IntegerField()
    price_30 = models.IntegerField(blank=True, null=True)

    price_14_owner = models.IntegerField(blank=True, null=True)
    price_30_owner = models.IntegerField(blank=True, null=True)
    phones = ArrayField(models.CharField(max_length=50),  10)
    # 
    location = models.ForeignKey("locations.Location", on_delete=models.CASCADE, null=True, blank=True, related_name="location_pr")
    # 
    category = models.ForeignKey("categories.category", on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey("categories.subcategory", on_delete=models.SET_NULL, null=True, blank=True)
    subcategory2 = models.ForeignKey("categories.sub_subcategory", on_delete=models.SET_NULL, null=True, blank=True)
    # 
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="my_product", null=True, blank=True)
    # 
    is_publish = models.BooleanField(default=False, blank=True, null=True)
    in_recomendation = models.BooleanField(default=False, blank=True, null=True)
    
    is_rented = models.BooleanField(default=False, blank=True)
    in_stock = models.BooleanField(default=False, blank=True)
    leave = models.BooleanField(default=False, blank=True)
    pickup = models.BooleanField(default=False, blank=True)
    # 
    count_day = models.IntegerField(blank=True, null=True)
    get_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    # 
    publish_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return self.title + ", " + str(self.id)
    

def product_photos_dir(instanse, filename):
    usrnme = f'{instanse.product.id}'
    folder_name = f"{usrnme}/{filename}"
    return folder_name

class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to=product_photos_dir, height_field=None, width_field=None)

    def __str__(self):
        return self.product.title


class Recomendation(models.Model):
    products = models.ManyToManyField("products.Product", related_name="recomendation")