from django.db import models


class category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey("category", on_delete=models.CASCADE, related_name="subcategory")

    def __str__(self):
        return self.name


class sub_subcategory(models.Model):
    name = models.CharField(max_length=50)
    subcategory = models.ForeignKey("subcategory", on_delete=models.CASCADE, related_name="sub_subcategory")

    def __str__(self):
        return self.name
