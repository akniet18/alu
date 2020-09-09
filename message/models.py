from django.db import models


class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="my_message")
    action = models.IntegerField(default=1)
    ownerorclient = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey("basket.Rented", on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    get_or_return = models.IntegerField(null=True, blank=True)
    is_readed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.user.phone + ", " + str(self.id)
