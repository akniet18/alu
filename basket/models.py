from django.db import models
# from products.models import *

class Rented(models.Model):
    TYPE_DELIVERY = 1
    TYPE_PICKUP = 2
    TYPE_GET_PRODUCT = (
        (TYPE_DELIVERY, 'Достовка'),
        (TYPE_PICKUP, 'Самовывоз')
    )

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="rented_product")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="i_rent")
    count_day = models.IntegerField()
    rented_day = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    get_product = models.SmallIntegerField(choices=TYPE_GET_PRODUCT, blank=True, null=True)
    is_rented = models.BooleanField(default=False, blank=True, null=True)
    is_ended = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return "user {}, {}".format(self.user.phone, self.product.title)

