from django.db import models
# from products.models import *

class Rented(models.Model):
    TYPE_DELIVERY = 1
    TYPE_PICKUP = 2
    TYPE_GET_PRODUCT = (
        (TYPE_DELIVERY, 'Достовка'),
        (TYPE_PICKUP, 'Самовывоз')
    )

    product = models.ManyToManyField("products.Product", blank=True, related_name="rented_obj")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="i_rent")
    amount = models.IntegerField()
    rented_day = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    get_product = models.SmallIntegerField(choices=TYPE_GET_PRODUCT, blank=True, null=True)
    return_product = models.SmallIntegerField(choices=TYPE_GET_PRODUCT, blank=True, null=True)

    get_address = models.TextField(blank=True, null=True)
    return_address = models.TextField(blank=True, null=True)

    get_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)

    is_checked = models.BooleanField(default=False, blank=True, null=True)
    is_rented = models.BooleanField(default=False, blank=True, null=True)
    is_canceled = models.BooleanField(default=False, blank=True, null=True)
    is_ended = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return "id {}, user {}".format(self.id,self.user.phone)

